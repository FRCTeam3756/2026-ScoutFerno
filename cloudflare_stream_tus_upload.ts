import * as tus from "tus-js-client";

export type DirectUploadResponse = {
  upload_url: string;
  video_uid: string;
};

export type CloudflareStreamUploadOptions = {
  backendBaseUrl: string;
  file: File;
  maxDurationSeconds?: number;
  authToken?: string;
  onProgress?: (uploadedBytes: number, totalBytes: number) => void;
  onSuccess?: (result: DirectUploadResponse) => void;
};

async function createDirectUpload({
  backendBaseUrl,
  file,
  maxDurationSeconds = 600,
  authToken,
}: {
  backendBaseUrl: string;
  file: File;
  maxDurationSeconds?: number;
  authToken?: string;
}): Promise<DirectUploadResponse> {
  const response = await fetch(`${backendBaseUrl}/videos/direct-upload`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    },
    body: JSON.stringify({
      file_size: file.size,
      file_name: file.name,
      max_duration_seconds: maxDurationSeconds,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to create Cloudflare Stream upload URL: ${response.status} ${errorText}`
    );
  }

  return (await response.json()) as DirectUploadResponse;
}

export async function uploadVideoToCloudflareStream({
  backendBaseUrl,
  file,
  maxDurationSeconds = 600,
  authToken,
  onProgress,
  onSuccess,
}: CloudflareStreamUploadOptions): Promise<DirectUploadResponse> {
  const directUpload = await createDirectUpload({
    backendBaseUrl,
    file,
    maxDurationSeconds,
    authToken,
  });

  await new Promise<void>((resolve, reject) => {
    const upload = new tus.Upload(file, {
      uploadUrl: directUpload.upload_url,
      retryDelays: [0, 1000, 3000, 5000],
      removeFingerprintOnSuccess: true,
      metadata: {
        filename: file.name,
        filetype: file.type || "application/octet-stream",
      },
      headers: {
        "Tus-Resumable": "1.0.0",
      },
      onError: reject,
      onProgress: (uploadedBytes, totalBytes) => {
        onProgress?.(uploadedBytes, totalBytes);
      },
      onSuccess: () => {
        onSuccess?.(directUpload);
        resolve();
      },
    });

    upload.start();
  });

  return directUpload;
}

/*
Frontend usage example:

import { uploadVideoToCloudflareStream } from "./cloudflare_stream_tus_upload";

const result = await uploadVideoToCloudflareStream({
  backendBaseUrl: "http://127.0.0.1:8000",
  file,
  onProgress: (uploaded, total) => {
    const percent = Math.round((uploaded / total) * 100);
    console.log(`Upload progress: ${percent}%`);
  },
});

console.log("Cloudflare video UID:", result.video_uid);

Install dependency:
npm install tus-js-client
*/


<iframe
  src="https://customer-<YOUR_STREAM_CUSTOMER_CODE>.cloudflarestream.com/<VIDEO_UID>/iframe"
  style="border: none; width: 100%; aspect-ratio: 16 / 9;"
  allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;"
  allowfullscreen
></iframe>

