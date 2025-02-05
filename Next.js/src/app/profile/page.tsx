"use client";

import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { addProfile } from "@/actions/actions";
import { string, ZodIssue } from "zod";
import { resourceLimits } from "worker_threads";
import { error } from "console";

type AddProfileResult =
  | { success: true; message: string }
  | { success: false; errors: ZodIssue[] | string };

interface Project {
  description: string;
  techStack: string;
  portfolio: string;
}

export default function Profile() {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [background, setBackground] = useState<string>("");
  const [projects, setProjects] = useState<Project[]>([
    { description: "", techStack: "", portfolio: "" },
  ]);

  const { toast } = useToast();

  const handleAddProject = () => {
    setProjects([
      ...projects,
      { description: "", techStack: "", portfolio: "" },
    ]);
  };

  const handleRemoveProject = (index: number) => {
    if (projects.length > 1) {
      toast({
        variant: "destructive",
        title: "Removed Project",
        description: `${projects[index].description}`,
      });
      setProjects(projects.filter((_, i) => i !== index));
    }
  };

  const handleChange = (index: number, field: keyof Project, value: string) => {
    const newProjects = [...projects];
    newProjects[index][field] = value;
    setProjects(newProjects);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("background", background);
    formData.append("projects", JSON.stringify(projects)); // Serialize array

    const result: AddProfileResult = await addProfile(formData);

    if (result.success) {
      toast({ description: result.message });
    } else {
      if (typeof result.errors === "string") {
        toast({
          description: result.errors,
        });
      } else {
        toast({
          variant: "destructive",
          description: result.errors.map((err) => err.message).join(", "),
        });
      }
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 shadow-md rounded-md">
      <h2 className="text-2xl font-bold mb-6 text-center">
        Tell us about yourself
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name Field */}
        <div>
          <Input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="Name"
            name="name"
          />
        </div>

        {/* Email Field */}
        <div>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="Email"
            name="email"
          />
        </div>

        <div>
          <Textarea
            value={background}
            onChange={(e) => setBackground(e.target.value)}
            required
            placeholder="Background (Education, Work Experience,etc)"
            name="background"
          />
        </div>

        {/* Dynamic Project Fields */}
        {projects.map((project, index) => (
          <div key={index} className="p-4 border rounded-md space-y-2">
            <div className="flex justify-between items-center">
              <h3 className="font-medium text-md">Project {index + 1}</h3>
              {projects.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveProject(index)}
                  className="text-red-500 hover:text-red-700 text-xl font-bold"
                >
                  −
                </button>
              )}
            </div>
            <div>
              <Textarea
                value={project.description}
                onChange={(e) =>
                  handleChange(index, "description", e.target.value)
                }
                required
                placeholder="Project Description"
                name="description"
              />
            </div>
            <div>
              <Textarea
                value={project.techStack}
                onChange={(e) =>
                  handleChange(index, "techStack", e.target.value)
                }
                required
                placeholder="Tech Stack (e.g., React, Python, C++)"
                name="techStack"
              />
            </div>
            <div>
              <Input
                type="url"
                value={project.portfolio}
                onChange={(e) =>
                  handleChange(index, "portfolio", e.target.value)
                }
                placeholder="Link to the Project"
                name="portfolio"
              />
            </div>
          </div>
        ))}

        {/* Add More Projects Button */}
        <button
          type="button"
          onClick={handleAddProject}
          className="w-full flex items-center justify-center py-2 border rounded-md hover:bg-blue-800"
        >
          + Add Another Project
        </button>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full py-2 rounded-md border hover:bg-blue-800"
        >
          Submit
        </button>
      </form>
    </div>
  );
}
