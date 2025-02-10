"use server";
import axios from "axios";
import { z } from "zod";

const jobUrlSchema = z.string().url();
const idSchema = z.string().min(1);

export async function submitUrl(jobUrl: string, id: string) {
  try {
    const ValiadtedUrl = jobUrlSchema.parse(jobUrl);
    const ValidatedId = idSchema.parse(id);
    const resp = await axios.post(
      `${process.env.BACKEND_URL}/api/email/generate`,
      { url: ValiadtedUrl, id: ValidatedId }
    );
    const generatedEmail = resp.data.email;
    const message = resp.data.message;
    return {
      generatedEmail: generatedEmail,
      url: ValiadtedUrl,
      message: message,
    };
  } catch (error: any) {
    return {
      generatedEmail: "Failed to generate Email ",
      url: jobUrl || " ",
      message: error.message || "Failed to generate Email ",
    };
  }
}
