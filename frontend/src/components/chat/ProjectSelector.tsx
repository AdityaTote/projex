"use client";

import { Folder, Loader2, AlertCircle } from "lucide-react";
import { useProjects } from "@/hooks/useProjects";
import { useStore } from "@/store/useStore";

export default function ProjectSelector() {
  const { data: projects, isLoading, error } = useProjects();
  const setActiveProject = useStore((s) => s.setActiveProject);

  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 text-slate-400 animate-spin" />
          <p className="text-sm text-slate-500 font-medium">
            Loading projects...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4 text-center max-w-sm">
          <div className="w-12 h-12 bg-rose-50 rounded-2xl flex items-center justify-center">
            <AlertCircle className="w-6 h-6 text-rose-500" />
          </div>
          <p className="text-sm text-slate-700 font-semibold">
            Failed to load projects
          </p>
          <p className="text-xs text-slate-400">
            {error instanceof Error ? error.message : "Something went wrong"}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-lg shadow-blue-500/20">
            <Folder className="w-7 h-7 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Select a Project
          </h2>
          <p className="text-sm text-slate-500 mt-2">
            Choose a project to start a new chat session
          </p>
        </div>

        {/* Project Grid */}
        {projects && projects.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {projects.map((project) => (
              <button
                key={project.id}
                onClick={() =>
                  setActiveProject({ id: project.id, name: project.name })
                }
                className="group flex items-center gap-4 p-4 bg-white border border-slate-200 rounded-2xl text-left hover:border-blue-300 hover:shadow-md hover:shadow-blue-500/5 transition-all duration-200"
              >
                <div className="w-10 h-10 bg-slate-50 group-hover:bg-blue-50 rounded-xl flex items-center justify-center shrink-0 transition-colors">
                  <Folder className="w-5 h-5 text-slate-400 group-hover:text-blue-500 transition-colors" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-slate-800 truncate">
                    {project.name}
                  </p>
                  {project.status && (
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {project.status}
                    </p>
                  )}
                </div>
                <div className="w-2 h-2 bg-slate-200 group-hover:bg-blue-400 rounded-full shrink-0 transition-colors" />
              </button>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-sm text-slate-400">No projects found</p>
          </div>
        )}
      </div>
    </div>
  );
}
