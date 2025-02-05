"use server";

import { chromaClient } from "@/lib/chromaDbConnect";
import { log } from "console";
import { z } from "zod";
import { ZodIssue } from "zod";
import axios from "axios"


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

    const resp= await axios.post("http://localhost:8000/profile", validatedData)
    console.log(resp)

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
