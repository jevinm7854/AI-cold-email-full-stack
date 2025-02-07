"use server";
import axios from "axios";
import { z } from "zod";

const jobUrlSchema = z.string().url();

export async function submitUrl(jobUrl: string) {
  try {
    const ValiadtedUrl = jobUrlSchema.parse(jobUrl);
    const resp = await axios.post(
      `${process.env.BACKEND_URL}/api/email/generate`,
      { url: ValiadtedUrl }
    );
    const generatedEmail = resp.data.email;
    return { generatedEmail: generatedEmail, url: ValiadtedUrl };
  } catch (error) {
    return {
      generatedEmail: "Failed to generate Email ",
      url: "Please try again later",
    };
  }
}
