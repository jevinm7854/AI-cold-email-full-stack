"use server";

import { z } from "zod";
import { ZodIssue } from "zod";
import axios from "axios";
import { UUID } from "crypto";

type AddProfileResult =
  | { success: true; message: string; id: UUID }
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

    // Validate the extracted data
    const validatedData = profileSchema.parse({
      name,
      email,
      background,
      projects,
    });

    console.log("Validated Data:", validatedData);

    const resp = await axios.post(
      `${process.env.BACKEND_URL}/api/users/signup`,
      validatedData
    );
    console.log("Response:", resp);
    if (resp.status === 201) {
      return {
        success: true,
        id: resp.data.id,
        message: "Profile added successfully!",
      };
    } else {
      throw new Error("Failed to add profile");
    }
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors };
    }

    return { success: false, errors: error.message || "Something went wrong" };
  }
}
