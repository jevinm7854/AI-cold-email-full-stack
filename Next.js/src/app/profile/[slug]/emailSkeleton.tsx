import { Skeleton } from "@/components/ui/skeleton";

import React from "react";

function EmailSkeleton() {
  return (
    <div className="mt-4 w-full max-w-lg">
      <Skeleton className="h-10 w-full mb-4 rounded-md" />
      <Skeleton className="h-56 w-full rounded-md" />
    </div>
  );
}

export default EmailSkeleton;
