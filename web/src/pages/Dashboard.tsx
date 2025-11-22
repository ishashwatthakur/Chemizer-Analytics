import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ArrowLeft, User, Upload, LayoutDashboard, FileText, MoreVertical, Eye, Download, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/lib/api";
import { toast } from "sonner";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface UploadHistory {
  id: number;
  upload_id: string;
  filename: string;
  upload_date: string;
  upload_date_formatted: string;
  rows: number;
  status: string;
  file_size?: number;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [visibleCount, setVisibleCount] = useState(3);
  const [uploadsHistory, setUploadsHistory] = useState<UploadHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUploads, setSelectedUploads] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchUploadHistory();
  }, []);

  const fetchUploadHistory = async () => {
    setLoading(true);
    try {
      const result = await apiClient.getUploadHistory();
      
      if (result.error) {
        toast.error(result.error);
        setLoading(false);
        return;
      }

      if (result.data && (result.data as any).uploads) {
        setUploadsHistory((result.data as any).uploads);
      }
    } catch (error) {
      console.error('Failed to fetch upload history:', error);
      toast.error('Failed to load upload history');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadMore = () => {
    setVisibleCount(prev => Math.min(prev + 3, uploadsHistory.length));
  };

  const handleViewResults = (uploadId: string) => {
    localStorage.setItem('current_upload_id', uploadId);
    navigate("/results");
  };

  const handleDownloadPDF = async (uploadId: string) => {
    try {
      const blob = await apiClient.downloadPDFReport(uploadId);
      if (blob) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analysis_report_${uploadId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success('PDF downloaded successfully');
      }
    } catch (error) {
      toast.error('Failed to download PDF');
    }
  };

  const handleDeleteUpload = async (uploadId: string) => {
    if (!confirm('Are you sure you want to delete this upload? This action cannot be undone.')) {
      return;
    }
    try {
      const result = await apiClient.deleteUpload(uploadId);
      if (result.error) {
        toast.error(result.error);
        return;
      }
      setUploadsHistory(uploadsHistory.filter(u => u.upload_id !== uploadId));
      toast.success('Upload deleted successfully');
    } catch (error) {
      toast.error('Failed to delete upload');
    }
  };

  const toggleUploadSelection = (uploadId: string) => {
    const newSelected = new Set(selectedUploads);
    if (newSelected.has(uploadId)) {
      newSelected.delete(uploadId);
    } else {
      newSelected.add(uploadId);
    }
    setSelectedUploads(newSelected);
  };

  const handleBulkDelete = async () => {
    if (selectedUploads.size === 0) {
      toast.error('Please select files to delete');
      return;
    }
    if (!confirm(`Delete ${selectedUploads.size} selected uploads?`)) {
      return;
    }
    try {
      for (const uploadId of selectedUploads) {
        await apiClient.deleteUpload(uploadId);
      }
      setUploadsHistory(uploadsHistory.filter(u => !selectedUploads.has(u.upload_id)));
      setSelectedUploads(new Set());
      toast.success('Uploads deleted successfully');
    } catch (error) {
      toast.error('Failed to delete uploads');
    }
  };

  const handleBulkDownload = async () => {
    if (selectedUploads.size === 0) {
      toast.error('Please select files to download');
      return;
    }
    try {
      for (const uploadId of selectedUploads) {
        await handleDownloadPDF(uploadId);
      }
      toast.success(`Downloaded ${selectedUploads.size} reports`);
    } catch (error) {
      toast.error('Failed to download files');
    }
  };

  const totalRows = uploadsHistory.reduce((sum, item) => sum + item.rows, 0);
  const totalSize = uploadsHistory.reduce((sum, item) => sum + (item.file_size || 0), 0);

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 blur-backdrop border-b border-border">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Button
              variant="ghost"
              onClick={() => navigate("/")}
              className="rounded-md"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <h1 className="text-xl font-bold">Chemizer Analytics</h1>
          </div>
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => navigate("/main")}
              className="rounded-md"
            >
              <Upload className="h-4 w-4 mr-2" />
              Upload
            </Button>
            <Button
              variant="ghost"
              onClick={() => navigate("/dashboard")}
              className="rounded-md bg-secondary"
            >
              <LayoutDashboard className="h-4 w-4 mr-2" />
              Dashboard
            </Button>
            <Button
              variant="ghost"
              onClick={() => navigate("/profile")}
              className="rounded-md"
            >
              <User className="h-4 w-4 mr-2" />
              Profile
            </Button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="pt-24 pb-12 px-6">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold mb-2">Dashboard</h2>
          <p className="text-muted-foreground mb-8">
            View your upload history and access previous analysis results
          </p>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Total Uploads</p>
              <p className="text-3xl font-bold">{loading ? "..." : uploadsHistory.length}</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Total Data Points</p>
              <p className="text-3xl font-bold">
                {loading ? "..." : totalRows.toLocaleString()}
              </p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Total Storage Used</p>
              <p className="text-3xl font-bold">
                {loading ? "..." : `${(totalSize / 1024 / 1024).toFixed(2)} MB`}
              </p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Last Upload</p>
              <p className="text-3xl font-bold text-sm">
                {loading ? "..." : (uploadsHistory[0]?.upload_date_formatted || "No uploads")}
              </p>
            </div>
          </div>

          {/* Upload History */}
          <div className="bg-card border border-border rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">Upload History</h3>
              {selectedUploads.size > 0 && (
                <div className="flex gap-2">
                  <Button
                    onClick={handleBulkDownload}
                    variant="outline"
                    size="sm"
                    className="rounded-md"
                  >
                    <Download className="h-4 w-4 mr-1" />
                    Download ({selectedUploads.size})
                  </Button>
                  <Button
                    onClick={handleBulkDelete}
                    variant="destructive"
                    size="sm"
                    className="rounded-md"
                  >
                    <Trash2 className="h-4 w-4 mr-1" />
                    Delete ({selectedUploads.size})
                  </Button>
                </div>
              )}
            </div>
            {loading ? (
              <div className="text-center py-8 text-muted-foreground">
                Loading upload history...
              </div>
            ) : uploadsHistory.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                No uploads yet. Upload your first file to get started!
              </div>
            ) : (
              <>
                <div className="space-y-4">
                  {uploadsHistory.slice(0, visibleCount).map((upload) => (
                    <div
                      key={upload.id}
                      className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-secondary/50 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <input
                          type="checkbox"
                          checked={selectedUploads.has(upload.upload_id)}
                          onChange={() => toggleUploadSelection(upload.upload_id)}
                          className="w-4 h-4 rounded"
                        />
                        <div className="bg-accent/10 p-3 rounded-lg">
                          <FileText className="h-6 w-6 text-accent" />
                        </div>
                        <div>
                          <p className="font-medium">{upload.filename}</p>
                          <p className="text-sm text-muted-foreground">
                            {upload.upload_date_formatted} • {upload.rows} rows • {upload.status}
                          </p>
                        </div>
                      </div>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="rounded-md"
                          >
                            <MoreVertical className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="rounded-md">
                          <DropdownMenuItem onClick={() => handleViewResults(upload.upload_id)}>
                            <Eye className="h-4 w-4 mr-2" />
                            View
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleDownloadPDF(upload.upload_id)}>
                            <Download className="h-4 w-4 mr-2" />
                            Download PDF
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleDeleteUpload(upload.upload_id)} className="text-destructive">
                            <Trash2 className="h-4 w-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  ))}
                </div>

                {visibleCount < uploadsHistory.length && (
                  <div className="mt-6 text-center">
                    <Button
                      onClick={handleLoadMore}
                      variant="outline"
                      className="rounded-md"
                    >
                      Load More
                    </Button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
