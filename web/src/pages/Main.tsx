import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Upload, ArrowLeft, FileSpreadsheet, User, LayoutDashboard } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { apiClient } from "@/lib/api";

const Main = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const progressMessages = [
    "Uploading file...",
    "Parsing CSV data...",
    "Validating data types...",
    "Calculating statistics...",
    "Generating charts...",
    "Creating analysis...",
    "Finalizing results...",
  ];

  const getProgressMessage = () => {
    const messageIndex = Math.floor((progress / 100) * (progressMessages.length - 1));
    return progressMessages[Math.min(messageIndex, progressMessages.length - 1)];
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const validTypes = [
        'text/csv',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ];
      
      if (validTypes.includes(file.type)) {
        setSelectedFile(file);
        toast.success(`${file.name} selected`);
      } else {
        toast.error("Please select a valid CSV or Excel file");
      }
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) {
      toast.error("Please select a file first");
      return;
    }

    setUploading(true);
    setProgress(0);

    try {
      const result = await apiClient.uploadFile(selectedFile, (progress) => {
        setProgress(progress);
      });

      if (result.error) {
        toast.error(result.error);
        setUploading(false);
        setProgress(0);
        return;
      }

      if (result.data) {
        toast.success("Analysis completed!", {
          duration: 2000,
        });
        
        // Store upload ID for results page
        const data = result.data as any;
        const uploadId = data.upload_id || data.id;
        if (uploadId) {
          localStorage.setItem('current_upload_id', uploadId);
        }
        
        setTimeout(() => {
          setUploading(false);
          setProgress(0);
          navigate("/results");
        }, 2000);
      }
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Failed to upload file. Please try again.');
      setUploading(false);
      setProgress(0);
    }
  };

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
              className="rounded-md"
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
        <div className="container mx-auto max-w-2xl">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-2">Upload Equipment Data</h2>
            <p className="text-muted-foreground">
              Upload your CSV or Excel file to analyze equipment parameters
            </p>
            <p className="text-sm text-muted-foreground mt-2">
              Maximum file size: 5MB
            </p>
          </div>

          <div className="bg-card border border-border rounded-lg p-8">
            <div className="space-y-6">
              {/* File Upload Area */}
              <div className="border-2 border-dashed border-border rounded-lg p-12 text-center hover:border-accent transition-colors">
                <FileSpreadsheet className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                <p className="text-lg font-medium mb-2">
                  {selectedFile ? selectedFile.name : "Select a file to upload"}
                </p>
                <p className="text-sm text-muted-foreground mb-4">
                  CSV or Excel files supported
                </p>
                <input
                  type="file"
                  id="file-upload"
                  accept=".csv,.xlsx,.xls"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <Button
                  onClick={() => document.getElementById('file-upload')?.click()}
                  variant="outline"
                  className="rounded-md"
                >
                  Choose File
                </Button>
              </div>

              {/* Upload Button */}
              <Button
                onClick={handleUploadAndAnalyze}
                disabled={!selectedFile || uploading}
                className="w-full bg-primary text-primary-foreground hover:bg-primary/90 rounded-md"
                size="lg"
              >
                {uploading ? "Analyzing..." : "Upload and Analyze"}
              </Button>

              {/* Progress Info */}
              {selectedFile && (
                <div className="text-sm text-muted-foreground space-y-1">
                  <p><strong>File:</strong> {selectedFile.name}</p>
                  <p><strong>Size:</strong> {(selectedFile.size / 1024).toFixed(2)} KB</p>
                  <p><strong>Type:</strong> {selectedFile.type}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Upload Progress Modal */}
      {uploading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 blur-backdrop">
          <div className="bg-card border border-border rounded-lg p-8 max-w-md w-full mx-4 shadow-lg">
            <h3 className="text-xl font-bold mb-4 text-center">Analyzing Data</h3>
            <div className="space-y-4">
              <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
                <div
                  className="bg-accent h-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-center text-sm text-muted-foreground">
                {getProgressMessage()}
              </p>
              <p className="text-center text-xs text-muted-foreground">
                {progress}% complete
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Main;
