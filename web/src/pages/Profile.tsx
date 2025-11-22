import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, User, Upload, LayoutDashboard, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { apiClient } from "@/lib/api";

interface UploadHistory {
  id: number;
  upload_id: string;
  filename: string;
  upload_date: string;
  rows: number;
  status: string;
}

const Profile = () => {
  const navigate = useNavigate();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uploadsHistory, setUploadsHistory] = useState<UploadHistory[]>([]);
  const [formData, setFormData] = useState({
    fullName: "",
    username: "",
    email: "",
    dateOfBirth: "",
    gender: "",
  });

  useEffect(() => {
    fetchProfile();
    fetchUploadHistory();
  }, []);

  const fetchUploadHistory = async () => {
    try {
      const result = await apiClient.getUploadHistory();
      if (result.data && (result.data as any).uploads) {
        setUploadsHistory((result.data as any).uploads);
      }
    } catch (error) {
      console.error('Failed to fetch upload history:', error);
    }
  };

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const result = await apiClient.getProfile();
      if (result.error) {
        toast.error(result.error);
        return;
      }
      if (result.data) {
        const data = result.data as any;
        setFormData({
          fullName: data.full_name || "",
          username: data.username || "",
          email: data.email || "",
          dateOfBirth: data.date_of_birth || "",
          gender: data.gender || "",
        });
      }
    } catch (error) {
      toast.error('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const result = await apiClient.updateProfile({
        full_name: formData.fullName,
        date_of_birth: formData.dateOfBirth,
        gender: formData.gender,
      });
      if (result.error) {
        toast.error(result.error);
        return;
      }
      toast.success("Profile updated successfully");
      setEditing(false);
    } catch (error) {
      toast.error("Failed to update profile");
    }
  };

  const handleLogout = () => {
    apiClient.logout();
    toast.success("Logged out successfully");
    navigate("/auth/login");
  };

  const handleDeleteAccount = async () => {
    if (!confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
      return;
    }
    try {
      const result = await apiClient.deleteAccount();
      if (result.error) {
        toast.error(result.error);
        return;
      }
      toast.success("Account deleted successfully");
      navigate("/auth/login");
    } catch (error) {
      toast.error("Failed to delete account");
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
              className="rounded-md bg-secondary"
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
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">Profile</h2>
              <p className="text-muted-foreground">Manage your account information</p>
            </div>
            <Button
              onClick={handleLogout}
              variant="outline"
              className="rounded-md"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>

          {/* Profile Form */}
          <div className="bg-card border border-border rounded-lg p-6 mb-6">
            <div className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  disabled={!editing}
                  className="rounded-md"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  value={formData.username}
                  disabled={true}
                  className="rounded-md bg-secondary"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  disabled={true}
                  className="rounded-md bg-secondary"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="dateOfBirth">Date of Birth</Label>
                  <Input
                    id="dateOfBirth"
                    type="date"
                    value={formData.dateOfBirth}
                    onChange={(e) => setFormData({ ...formData, dateOfBirth: e.target.value })}
                    disabled={!editing}
                    className="rounded-md"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="gender">Gender</Label>
                  <Select
                    value={formData.gender}
                    onValueChange={(value) => setFormData({ ...formData, gender: value })}
                    disabled={!editing}
                  >
                    <SelectTrigger className="rounded-md">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex gap-4">
                {!editing ? (
                  <Button
                    onClick={() => setEditing(true)}
                    className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-md"
                  >
                    Edit Profile
                  </Button>
                ) : (
                  <>
                    <Button
                      onClick={handleSave}
                      className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-md"
                    >
                      Save Changes
                    </Button>
                    <Button
                      onClick={() => setEditing(false)}
                      variant="outline"
                      className="rounded-md"
                    >
                      Cancel
                    </Button>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Data Management */}
          <div className="bg-card border border-border rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">Statistics</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-secondary/30 rounded-lg p-4">
                <p className="text-sm text-muted-foreground">Total Files Analyzed</p>
                <p className="text-2xl font-bold">{uploadsHistory.length}</p>
              </div>
              <div className="bg-secondary/30 rounded-lg p-4">
                <p className="text-sm text-muted-foreground">Total Files Uploaded</p>
                <p className="text-2xl font-bold">{uploadsHistory.length}</p>
              </div>
            </div>
          </div>

          {/* Data Download/Export */}
          <div className="bg-card border border-border rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold mb-2">Data Management</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Download a copy of all your analyzed files or permanently delete all data.
            </p>
            <div className="flex gap-4">
              <Button
                onClick={async () => {
                  try {
                    const blob = await apiClient.downloadAllData();
                    if (blob) {
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = `all_uploads_${new Date().toISOString().split('T')[0]}.csv`;
                      document.body.appendChild(a);
                      a.click();
                      window.URL.revokeObjectURL(url);
                      document.body.removeChild(a);
                      toast.success('All data downloaded successfully');
                    }
                  } catch (error) {
                    toast.error('Failed to download data');
                  }
                }}
                variant="outline"
                className="rounded-md"
              >
                Download All Data
              </Button>
              <Button
                onClick={async () => {
                  if (!confirm('Are you sure you want to delete ALL your uploaded data? This cannot be undone.')) {
                    return;
                  }
                  try {
                    const result = await apiClient.deleteAllData();
                    if (result.error) {
                      toast.error(result.error);
                      return;
                    }
                    setUploadsHistory([]);
                    toast.success('All data deleted successfully');
                  } catch (error) {
                    toast.error('Failed to delete data');
                  }
                }}
                variant="outline"
                className="rounded-md text-destructive"
              >
                Delete All Data
              </Button>
            </div>
          </div>

          {/* Account Management */}
          <div className="bg-destructive/5 border border-destructive/20 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">Account Management</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Once you delete your account, there is no going back. All your data will be permanently removed.
            </p>
            <Button
              onClick={handleDeleteAccount}
              variant="destructive"
              className="rounded-md"
            >
              Delete Account
            </Button>
          </div>

          {/* Upload History Stats */}
          <div className="bg-card border border-border rounded-lg p-6 mt-6" id="uploads-stats">
            <h3 className="text-lg font-semibold mb-4">Recent Uploads</h3>
            {uploadsHistory.length === 0 ? (
              <p className="text-sm text-muted-foreground">No uploads yet</p>
            ) : (
              <div className="space-y-2">
                {uploadsHistory.slice(0, 5).map((upload, idx) => (
                  <div key={idx} className="flex justify-between items-center p-2 border-b border-border last:border-0">
                    <span className="text-sm">{upload.filename}</span>
                    <span className="text-xs text-muted-foreground">{upload.rows} rows</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
