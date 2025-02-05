"use server";

import { chromaClient } from "@/lib/chromaDbConnect";
import { log } from "console";
import { z } from "zod";
import { ZodIssue } from "zod";
import { embed } from "chromadb-default-embed";

type AddProfileResult =
  | { success: true; message: string }
  | { success: false; errors: ZodIssue[] | string };

// Define the schema using Zod
const profileSchema = z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email format"),
  background: z.string().min(1, "Background is required"),
  projects: z.array(
    z.object({
      description: z.string().min(1, "Project description is required"),
      techStack: z.string().min(1, "Tech Stack is required"),
      portfolio: z.string().url("Invalid URL format").or(z.literal("")),
    })
  ),
});

export async function addProfile(
  formdata: FormData
): Promise<AddProfileResult> {
  try {
    const name = formdata.get("name") as string;
    const email = formdata.get("email") as string;
    const background = formdata.get("background") as string;
    const projects = JSON.parse(formdata.get("projects") as string);
    console.log("*********** ", projects);
    // Validate the extracted data
    const validatedData = profileSchema.parse({
      name,
      email,
      background,
      projects,
    });

    console.log("Validated Data:", validatedData);

    const collection = await chromaClient.getOrCreateCollection({
      name: name,
    });

    await collection.upsert({
      documents: [
        "This is a document about pineapple",
        "This is a document about oranges",
      ],
      ids: ["id1", "id2"],
    });

    const results = await collection.query({
      queryTexts: "This is a query document about citrus fruit", // Chroma will embed this for you
      nResults: 2, // how many results to return
    });

    console.log(results);

    return { success: true, message: "Profile added successfully!" };
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("Validation errors:", error.errors);
      return { success: false, errors: error.errors };
    }
    console.error("Unexpected error:", error);
    return { success: false, errors: "Something went wrong" };
  }
}
