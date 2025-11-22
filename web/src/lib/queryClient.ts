import { QueryClient } from "@tanstack/react-query";

async function handleResponse(response: Response) {
  if (response.ok) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    }
    return await response.text();
  }

  let errorMessage = `Request failed: ${response.status} ${response.statusText}`;
  
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    const errorData = await response.json();
    errorMessage = errorData.message || JSON.stringify(errorData);
  }

  throw new Error(errorMessage);
}

export async function apiRequest(url: string, options?: RequestInit) {
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    credentials: "include",
  });

  return handleResponse(response);
}

async function fetchApi(url: string) {
  const response = await fetch(url, {
    credentials: "include",
  });
  return handleResponse(response);
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: async ({ queryKey }) => {
        const url = queryKey[0] as string;
        return fetchApi(url);
      },
      staleTime: 1000 * 60 * 5,
      retry: false,
    },
  },
});
