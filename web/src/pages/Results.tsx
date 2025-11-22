import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Download, User, LayoutDashboard, Upload, ChevronDown } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, ComposedChart } from "recharts";
import { toast } from "sonner";
import { apiClient } from "@/lib/api";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";

const Results = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [uploadData, setUploadData] = useState<any>(null);
  const [dataPreview, setDataPreview] = useState<any[]>([]);
  const [showAllRows, setShowAllRows] = useState(false);

  useEffect(() => {
    const uploadId = localStorage.getItem('current_upload_id');
    if (!uploadId) {
      toast.error('No upload data found');
      navigate('/dashboard');
      return;
    }
    fetchUploadDetails(uploadId);
  }, []);

  const fetchUploadDetails = async (uploadId: string) => {
    setLoading(true);
    try {
      const result = await apiClient.getUploadDetail(uploadId);
      
      if (result.error) {
        toast.error(result.error);
        navigate('/dashboard');
        return;
      }

      if (result.data) {
        setUploadData(result.data);
        setDataPreview((result.data as any).data_preview || []);
      }
    } catch (error) {
      console.error('Failed to fetch upload details:', error);
      toast.error('Failed to load analysis results');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    const uploadId = localStorage.getItem('current_upload_id');
    if (!uploadId) {
      toast.error('No upload ID found');
      return;
    }

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
      } else {
        toast.error('Failed to download PDF');
      }
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download PDF report');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-muted-foreground">Loading analysis results...</p>
        </div>
      </div>
    );
  }

  const summaryStats = uploadData?.summary_stats || {};
  const columns = uploadData?.column_names || [];
  const numericColumns = (summaryStats && typeof summaryStats === 'object' && !Array.isArray(summaryStats)) 
    ? Object.keys(summaryStats) 
    : [];

  const generateSummary = () => {
    if (!uploadData) return '';
    const totalRows = uploadData.rows || 0;
    const totalColumns = uploadData.columns || 0;
    const numericCols = numericColumns.length;
    
    return `This analysis includes ${totalRows.toLocaleString()} rows of equipment data across ${totalColumns} columns, with ${numericCols} numeric parameters. The data has been processed to extract key insights about equipment performance metrics, including statistical distributions and correlations between parameters.`;
  };

  const getNumericColumnData = (columnName: string) => {
    return dataPreview.slice(0, 20).map((row: any, idx: number) => ({
      name: `${idx + 1}`,
      value: parseFloat(row[columnName]) || 0
    }));
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 blur-backdrop border-b border-border">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Button
              variant="ghost"
              onClick={() => navigate("/main")}
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
        <div className="container mx-auto max-w-7xl">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">Analysis Results</h2>
              <p className="text-muted-foreground">
                Equipment data analysis and visualization
              </p>
            </div>
            <Button
              onClick={handleDownloadPDF}
              className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-md"
            >
              <Download className="h-4 w-4 mr-2" />
              Download PDF Report
            </Button>
          </div>

          {/* Summary Section */}
          <div className="bg-card border border-border rounded-lg p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4">Summary</h3>
            <p className="text-muted-foreground leading-relaxed">
              {generateSummary()}
            </p>
          </div>

          {/* Statistics */}
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Total Rows</p>
              <p className="text-3xl font-bold">{uploadData?.rows || 0}</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Total Columns</p>
              <p className="text-3xl font-bold">{uploadData?.columns || 0}</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">Numeric Columns</p>
              <p className="text-3xl font-bold">{numericColumns.length}</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <p className="text-sm text-muted-foreground mb-1">File Size</p>
              <p className="text-3xl font-bold">{((uploadData?.file_size || 0) / 1024).toFixed(1)} KB</p>
            </div>
          </div>

          {/* Highlighted Points */}
          <div className="bg-secondary/30 border border-border rounded-lg p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4">Highlighted Insights</h3>
            <ul className="space-y-2 text-sm">
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold">•</span>
                <span>Dataset contains {dataPreview.length} records available for detailed analysis</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold">•</span>
                <span>{numericColumns.length} numeric columns identified for statistical analysis</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-accent font-bold">•</span>
                <span>File size: {((uploadData?.file_size || 0) / 1024).toFixed(2)} KB</span>
              </li>
            </ul>
          </div>

          {/* Data Preview */}
          {dataPreview.length > 0 && (
            <div className="bg-card border border-border rounded-lg p-6 mb-8">
              <h3 className="text-xl font-semibold mb-4">Data Preview</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border">
                      {columns.map((col: string) => (
                        <th key={col} className="text-left p-2 font-medium">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {dataPreview.slice(0, showAllRows ? dataPreview.length : 20).map((row: any, idx: number) => (
                      <tr key={idx} className="border-b border-border hover:bg-secondary/50">
                        {columns.map((col: string) => (
                          <td key={col} className="p-2">{String(row[col] || 'N/A')}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {dataPreview.length > 20 && (
                <div className="mt-4 text-center">
                  <Button
                    onClick={() => setShowAllRows(!showAllRows)}
                    variant="outline"
                    className="rounded-md"
                  >
                    {showAllRows ? 'Show Less' : `Load More (${dataPreview.length - 20} more rows)`}
                  </Button>
                </div>
              )}
            </div>
          )}

          {/* Graphs Section */}
          {numericColumns.length > 0 && (
            <div className="space-y-8 mb-8">
              <h3 className="text-xl font-semibold mt-8">Graphs</h3>
              {numericColumns.slice(0, 3).map((col, idx) => (
                <Collapsible key={col} defaultOpen={idx === 0}>
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 bg-card border border-border rounded-lg hover:bg-secondary/50">
                    <ChevronDown className="h-4 w-4" />
                    <span className="font-semibold">{col} - Line Chart</span>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="bg-card border border-t-0 border-border rounded-b-lg p-6">
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={getNumericColumnData(col)}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" stroke="hsl(var(--foreground))" />
                        <YAxis stroke="hsl(var(--foreground))" />
                        <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "0.5rem" }} />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke="hsl(var(--accent))" name={col} />
                      </LineChart>
                    </ResponsiveContainer>
                  </CollapsibleContent>
                </Collapsible>
              ))}
            </div>
          )}

          {/* Charts Section */}
          {numericColumns.length > 0 && (
            <div className="space-y-8 mb-8">
              <h3 className="text-xl font-semibold mt-8">Charts</h3>
              
              {/* Bar Chart */}
              <Collapsible defaultOpen={true}>
                <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 bg-card border border-border rounded-lg hover:bg-secondary/50">
                  <ChevronDown className="h-4 w-4" />
                  <span className="font-semibold">Bar Chart - {numericColumns[0]}</span>
                </CollapsibleTrigger>
                <CollapsibleContent className="bg-card border border-t-0 border-border rounded-b-lg p-6">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getNumericColumnData(numericColumns[0])}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                      <XAxis dataKey="name" stroke="hsl(var(--foreground))" />
                      <YAxis stroke="hsl(var(--foreground))" />
                      <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "0.5rem" }} />
                      <Legend />
                      <Bar dataKey="value" fill="hsl(var(--accent))" name={numericColumns[0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CollapsibleContent>
              </Collapsible>

              {/* Pie Chart */}
              {numericColumns.length > 1 && (
                <Collapsible>
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 bg-card border border-border rounded-lg hover:bg-secondary/50">
                    <ChevronDown className="h-4 w-4" />
                    <span className="font-semibold">Pie Chart - {numericColumns[1]}</span>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="bg-card border border-t-0 border-border rounded-b-lg p-6">
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie data={getNumericColumnData(numericColumns[1])} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} fill="hsl(var(--accent))">
                          {getNumericColumnData(numericColumns[1]).map((entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={`hsl(${index * 60}, 70%, 50%)`} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "0.5rem" }} />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </CollapsibleContent>
                </Collapsible>
              )}

              {/* Histogram */}
              {numericColumns.length > 2 && (
                <Collapsible>
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 bg-card border border-border rounded-lg hover:bg-secondary/50">
                    <ChevronDown className="h-4 w-4" />
                    <span className="font-semibold">Histogram - {numericColumns[2]}</span>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="bg-card border border-t-0 border-border rounded-b-lg p-6">
                    <ResponsiveContainer width="100%" height={300}>
                      <ComposedChart data={getNumericColumnData(numericColumns[2])}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" stroke="hsl(var(--foreground))" />
                        <YAxis stroke="hsl(var(--foreground))" />
                        <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "0.5rem" }} />
                        <Legend />
                        <Bar dataKey="value" fill="hsl(var(--accent))" name={numericColumns[2]} />
                      </ComposedChart>
                    </ResponsiveContainer>
                  </CollapsibleContent>
                </Collapsible>
              )}

              {/* Scatter Plot */}
              {numericColumns.length > 0 && (
                <Collapsible>
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 bg-card border border-border rounded-lg hover:bg-secondary/50">
                    <ChevronDown className="h-4 w-4" />
                    <span className="font-semibold">Scatter Plot - Data Distribution</span>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="bg-card border border-t-0 border-border rounded-b-lg p-6">
                    <ResponsiveContainer width="100%" height={300}>
                      <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" name="Index" stroke="hsl(var(--foreground))" />
                        <YAxis dataKey="value" name={numericColumns[0]} stroke="hsl(var(--foreground))" />
                        <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "0.5rem" }} />
                        <Legend />
                        <Scatter name={numericColumns[0]} data={getNumericColumnData(numericColumns[0])} fill="hsl(var(--accent))" />
                      </ScatterChart>
                    </ResponsiveContainer>
                  </CollapsibleContent>
                </Collapsible>
              )}

              {/* Combined Chart (Line + Bar) */}
              {numericColumns.length > 1 && (
                <Collapsible>
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 bg-card border border-border rounded-lg hover:bg-secondary/50">
                    <ChevronDown className="h-4 w-4" />
                    <span className="font-semibold">Combined Chart - Multiple Parameters</span>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="bg-card border border-t-0 border-border rounded-b-lg p-6">
                    <ResponsiveContainer width="100%" height={300}>
                      <ComposedChart data={getNumericColumnData(numericColumns[0])}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="name" stroke="hsl(var(--foreground))" />
                        <YAxis stroke="hsl(var(--foreground))" />
                        <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "0.5rem" }} />
                        <Legend />
                        <Bar dataKey="value" fill="hsl(var(--accent))" name={numericColumns[0]} />
                        <Line type="monotone" dataKey="value" stroke="hsl(var(--primary))" name={numericColumns[1] || 'Value'} />
                      </ComposedChart>
                    </ResponsiveContainer>
                  </CollapsibleContent>
                </Collapsible>
              )}
            </div>
          )}

          {/* Calculations Section */}
          <div className="bg-card border border-border rounded-lg p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4">Calculations & Statistics</h3>
            <div className="space-y-6">
              {numericColumns.map((col) => (
                <Collapsible key={col}>
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-3 bg-secondary/30 rounded-lg hover:bg-secondary/50">
                    <ChevronDown className="h-4 w-4" />
                    <span className="font-semibold">{col}</span>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="p-4 bg-secondary/10 rounded-b-lg">
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                      {summaryStats[col] && (
                        <>
                          <div><strong>Mean:</strong> {(summaryStats[col].mean || 0).toFixed(2)}</div>
                          <div><strong>Median:</strong> {(summaryStats[col].median || 0).toFixed(2)}</div>
                          <div><strong>Std Dev:</strong> {(summaryStats[col].std || 0).toFixed(2)}</div>
                          <div><strong>Min:</strong> {(summaryStats[col].min || 0).toFixed(2)}</div>
                          <div><strong>Max:</strong> {(summaryStats[col].max || 0).toFixed(2)}</div>
                          <div><strong>Count:</strong> {summaryStats[col].count || 0}</div>
                        </>
                      )}
                    </div>
                  </CollapsibleContent>
                </Collapsible>
              ))}
            </div>
          </div>

          {/* Column Info */}
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-4">Column Information</h3>
            <div className="space-y-2">
              {columns.map((col: string) => (
                <div key={col} className="flex justify-between items-center p-2 border-b border-border last:border-0">
                  <span className="font-medium">{col}</span>
                  <span className="text-muted-foreground text-sm">
                    {uploadData?.data_types?.[col] || 'Unknown'} • Missing: {uploadData?.missing_values?.[col] || 0}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
