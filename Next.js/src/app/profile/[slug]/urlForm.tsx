"use client";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import Form from "next/form";
import { Button } from "@/components/ui/button";
import { submitUrl } from "@/actions/generateEmail-actions";
import { Skeleton } from "@/components/ui/skeleton";
import Loader from "@/components/ui/loader";
import EmailSkeleton from "./emailSkeleton";
import { Clipboard } from "lucide-react";
import { toast, useToast } from "@/hooks/use-toast";
import { z } from "zod";

export default function UrlForm() {
  const [genEmail, setGenEmail] = useState<string | null>(null);
  const [url, setUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const copyToClipboard = (type: string, text: string) => {
    navigator.clipboard.writeText(text);
    toast({ title: `Copied ${type} to clipboard` });
  };

  const jobUrlSchema = z.string().url();

  const handleSubmit = async (formData: FormData) => {
    // Validate URL
    try {
      jobUrlSchema.parse(formData.get("url"));
    } catch (error) {
      toast({ variant: "destructive", title: "Invalid URL" });
      return;
    }

    setLoading(true); // Start loading
    setGenEmail(null); // Clear previous results
    // setUrl(null); // Clear previous results

    setTimeout(async () => {
      const response = await submitUrl(formData.get("url") as string);
      const email = response.generatedEmail;
      const url = response.url;
      setGenEmail(email);
      setUrl(url);
      setLoading(false); // Stop loading
    }, 1); // Slight delay to trigger UI update
  };

  return (
    <div className="flex flex-col items-center pt-4 space-y-6 w-full max-w-lg mx-auto">
      <Form action={handleSubmit} className="w-full max-w-lg">
        <Input
          name="url"
          type="text"
          placeholder="Enter URL"
          className="w-full p-3 mb-4 border rounded-md"
        />
        <Button
          type="submit"
          className="w-full p-3 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Generate Email
        </Button>
      </Form>

      {loading ? (
        // <div className="flex justify-center items-center w-full">
        //   <Loader />
        // </div>
        <EmailSkeleton />
      ) : (
        <>
          {url && (
            <div className="relative mt-4 p-4 w-full max-w-lg border rounded-md shadow-lg bg-gray-200">
              {/* Copy Button for URL */}
              <Button
                onClick={() => copyToClipboard("url", url)}
                variant="ghost"
                size="icon"
                className="absolute top-2 right-2 p-1"
              >
                <Clipboard className="w-5 h-5 text-gray-500 hover:text-gray-700" />
              </Button>
              <p className="text-sm text-gray-600">{url}</p>
            </div>
          )}
          {genEmail && (
            <div className="relative mt-4 p-6 w-full max-w-lg border rounded-md shadow-lg bg-gray-200">
              {/* Copy Button for Email */}
              <Button
                onClick={() => copyToClipboard("email", genEmail)}
                variant="ghost"
                size="icon"
                className="absolute top-2 right-2 p-1"
              >
                <Clipboard className="w-5 h-5 text-gray-500 hover:text-gray-700" />
              </Button>
              <p className="text-sm text-gray-600">{genEmail}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
