import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Navigation } from '@/components/Navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { MoreVertical, Eye, Download, Trash2, Share2, Search } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { apiClient } from '../lib/api';
import { useNavigate } from 'react-router-dom';

interface UploadItem {
  id: number;
  upload_id: string;
  filename: string;
  upload_date: string;
  upload_date_formatted: string;
  rows: number;
  status: string;
}

export default function History() {
  const { token, isAuthenticated } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const [uploads, setUploads] = useState<UploadItem[]>([]);
  const [filteredUploads, setFilteredUploads] = useState<UploadItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/auth/login');
      return;
    }
    fetchHistory();
  }, [isAuthenticated]);

  useEffect(() => {
    if (searchTerm) {
      const filtered = uploads.filter((upload) =>
        upload.filename.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredUploads(filtered);
    } else {
      setFilteredUploads(uploads);
    }
  }, [searchTerm, uploads]);

  const fetchHistory = async () => {
    setIsLoading(true);
    try {
      const result = await apiClient.getUploadHistory();
      if (result.error) {
        toast({
          title: 'Error',
          description: result.error,
          variant: 'destructive',
        });
        return;
      }
      if (result.data && result.data.uploads) {
        setUploads(result.data.uploads);
        setFilteredUploads(result.data.uploads);
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to load upload history',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleView = (uploadId: string) => {
    navigate(`/results?upload_id=${uploadId}`);
  };

  const handleDownload = async (uploadId: string) => {
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
        toast({
          title: 'Success',
          description: 'PDF report downloaded successfully',
        });
      } else {
        toast({
          title: 'Error',
          description: 'Failed to download PDF',
          variant: 'destructive',
        });
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to download PDF report',
        variant: 'destructive',
      });
    }
  };

  const handleDelete = async (uploadId: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }

    try {
      const result = await apiClient.deleteUpload(uploadId);
      if (result.error) {
        toast({
          title: 'Error',
          description: result.error,
          variant: 'destructive',
        });
        return;
      }
      toast({
        title: 'Success',
        description: 'Upload deleted successfully',
      });
      fetchHistory();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete upload',
        variant: 'destructive',
      });
    }
  };

  const handleShare = (uploadId: string) => {
    const shareUrl = `${window.location.origin}/results?upload_id=${uploadId}`;
    navigator.clipboard.writeText(shareUrl);
    toast({
      title: 'Success',
      description: 'Share link copied to clipboard',
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col gap-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight" data-testid="text-page-title">Upload History</h1>
            <p className="text-muted-foreground" data-testid="text-page-description">
              View and manage all your past uploads
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search by filename..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
                data-testid="input-search"
              />
            </div>
          </div>

          {isLoading ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground" data-testid="text-loading">Loading history...</p>
            </div>
          ) : filteredUploads.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-muted-foreground" data-testid="text-no-uploads">
                  {searchTerm ? 'No uploads match your search' : 'No uploads yet'}
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {filteredUploads.map((upload) => (
                <Card key={upload.id} className="hover-elevate" data-testid={`card-upload-${upload.id}`}>
                  <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-3">
                    <div className="flex-1 min-w-0">
                      <CardTitle className="text-base truncate" data-testid={`text-filename-${upload.id}`}>
                        {upload.filename}
                      </CardTitle>
                      <CardDescription data-testid={`text-date-${upload.id}`}>
                        {upload.upload_date_formatted}
                      </CardDescription>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" data-testid={`button-menu-${upload.id}`}>
                          <MoreVertical className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => handleView(upload.upload_id)} data-testid={`button-view-${upload.id}`}>
                          <Eye className="mr-2 h-4 w-4" />
                          View
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleDownload(upload.upload_id)} data-testid={`button-download-${upload.id}`}>
                          <Download className="mr-2 h-4 w-4" />
                          Download PDF
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleShare(upload.upload_id)} data-testid={`button-share-${upload.id}`}>
                          <Share2 className="mr-2 h-4 w-4" />
                          Share Link
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => handleDelete(upload.upload_id, upload.filename)}
                          className="text-destructive"
                          data-testid={`button-delete-${upload.id}`}
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-muted-foreground" data-testid={`text-rows-${upload.id}`}>
                        {upload.rows.toLocaleString()} rows
                      </div>
                      <Badge variant={upload.status === 'Completed' ? 'default' : 'secondary'} data-testid={`badge-status-${upload.id}`}>
                        {upload.status}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
