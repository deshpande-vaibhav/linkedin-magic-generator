"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Wand2, MessageSquare, Image as ImageIcon, Sparkles, Send, Copy, Check, Loader2 } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<"comment" | "caption">("comment");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [copied, setCopied] = useState(false);

  // Form States - Comment
  const [postCaption, setPostCaption] = useState("");
  const [postLink, setPostLink] = useState("");
  const [profileLink, setProfileLink] = useState("");
  const [tone, setTone] = useState("Supportive");
  const [model, setModel] = useState("mistral-large-latest");

  // Form States - Caption
  const [thoughts, setThoughts] = useState("");
  const [captionProfileLink, setCaptionProfileLink] = useState("");
  const [mediaFile, setMediaFile] = useState<File | null>(null);
  const [mediaUrl, setMediaUrl] = useState("");

  const handleCopy = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const generateComment = async () => {
    if (!postCaption) return;
    setLoading(true);
    setResult("");
    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          post_caption: postCaption,
          post_link: postLink,
          profile_link: profileLink,
          tone,
          model
        }),
      });
      const data = await response.json();
      setResult(data.comment);
    } catch (error) {
      setResult("Error generating comment. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const generateCaption = async () => {
    if (!thoughts) return;
    setLoading(true);
    setResult("");
    try {
      const formData = new FormData();
      formData.append("thoughts", thoughts);
      formData.append("profile_link", captionProfileLink);
      formData.append("media_url", mediaUrl);
      if (mediaFile) {
        formData.append("media_file", mediaFile);
      }
      formData.append("model", model);

      const response = await fetch("/api/generate_caption", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data.caption);
    } catch (error) {
      setResult("Error generating caption. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4 md:p-8 flex flex-col items-center justify-start bg-premium-bg font-outfit">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12 mt-8"
      >
        <div className="flex items-center justify-center mb-4">
          <div className="bg-linkedin-blue p-3 rounded-2xl shadow-lg shadow-linkedin-blue/20">
            <Wand2 className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-2">
          LinkedIn Magic <span className="text-linkedin-blue">Generator</span>
        </h1>
        <p className="text-slate-500 text-lg font-medium">
          Elevate your engagement with AI-powered premium social content
        </p>
      </motion.div>

      {/* Main Container */}
      <div className="w-full max-w-3xl">
        {/* Tabs */}
        <div className="flex p-1.5 bg-slate-200/50 backdrop-blur-sm rounded-2xl mb-8 items-center justify-center gap-2">
          <button
            onClick={() => { setActiveTab("comment"); setResult(""); }}
            className={cn(
              "flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-bold transition-all duration-300",
              activeTab === "comment" ? "bg-white shadow-sm text-linkedin-blue" : "text-slate-500 hover:bg-white/50"
            )}
          >
            <MessageSquare size={18} />
            Comment Magic
          </button>
          <button
            onClick={() => { setActiveTab("caption"); setResult(""); }}
            className={cn(
              "flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-bold transition-all duration-300",
              activeTab === "caption" ? "bg-white shadow-sm text-linkedin-blue" : "text-slate-500 hover:bg-white/50"
            )}
          >
            <ImageIcon size={18} />
            Caption Magic
          </button>
        </div>

        {/* Form Card */}
        <motion.div 
          layout
          className="premium-card p-6 md:p-10 mb-8"
        >
          <AnimatePresence mode="wait">
            {activeTab === "comment" ? (
              <motion.div
                key="comment"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="space-y-6"
              >
                <div className="space-y-2">
                  <label className="text-sm font-bold text-slate-700 ml-1">Post Caption</label>
                  <textarea
                    value={postCaption}
                    onChange={(e) => setPostCaption(e.target.value)}
                    placeholder="Paste the LinkedIn post caption here..."
                    className="w-full h-32 glass-input resize-none"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">Post Link (Optional)</label>
                    <input
                      type="text"
                      value={postLink}
                      onChange={(e) => setPostLink(e.target.value)}
                      placeholder="https://linkedin.com/posts/..."
                      className="w-full glass-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">Profile Link (Optional)</label>
                    <input
                      type="text"
                      value={profileLink}
                      onChange={(e) => setProfileLink(e.target.value)}
                      placeholder="https://linkedin.com/in/..."
                      className="w-full glass-input"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">Tone</label>
                    <select
                      value={tone}
                      onChange={(e) => setTone(e.target.value)}
                      className="w-full glass-input appearance-none bg-white"
                    >
                      {["Supportive", "Professional", "Insightful", "Casual", "Funny", "Questioning"].map(t => (
                        <option key={t}>{t}</option>
                      ))}
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">AI Model</label>
                    <select
                      value={model}
                      onChange={(e) => setModel(e.target.value)}
                      className="w-full glass-input appearance-none bg-white"
                    >
                      <option value="mistral-large-latest">Mistral Large (Smartest)</option>
                      <option value="mistral-small-latest">Mistral Small (Fastest)</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={generateComment}
                  disabled={loading || !postCaption}
                  className="w-full btn-primary flex items-center justify-center gap-2 group"
                >
                  {loading ? <Loader2 className="animate-spin" /> : <Sparkles className="group-hover:scale-125 transition-transform" size={20} />}
                  Generate Magic Comment
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="caption"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="space-y-6"
              >
                <div className="space-y-2">
                  <label className="text-sm font-bold text-slate-700 ml-1">Your Thoughts / Topic</label>
                  <textarea
                    value={thoughts}
                    onChange={(e) => setThoughts(e.target.value)}
                    placeholder="What is this post about? Add your key messages here..."
                    className="w-full h-32 glass-input resize-none"
                  />
                </div>

                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">Media (Image/Video)</label>
                    <input
                      type="file"
                      onChange={(e) => setMediaFile(e.target.files?.[0] || null)}
                      className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-bold file:bg-linkedin-light file:text-linkedin-blue hover:file:bg-blue-100 transition-all"
                    />
                  </div>
                  <div className="relative flex items-center py-2">
                    <div className="flex-grow border-t border-slate-200"></div>
                    <span className="flex-shrink mx-4 text-slate-400 font-bold text-xs uppercase tracking-widest">OR</span>
                    <div className="flex-grow border-t border-slate-200"></div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">Direct Link to Media</label>
                    <input
                      type="text"
                      value={mediaUrl}
                      onChange={(e) => setMediaUrl(e.target.value)}
                      placeholder="Image/Video URL (Drive, Cloud, etc.)"
                      className="w-full glass-input"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">Profile Link (Optional)</label>
                    <input
                      type="text"
                      value={captionProfileLink}
                      onChange={(e) => setCaptionProfileLink(e.target.value)}
                      placeholder="https://linkedin.com/in/..."
                      className="w-full glass-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700 ml-1">AI Model</label>
                    <select
                      value={model}
                      onChange={(e) => setModel(e.target.value)}
                      className="w-full glass-input appearance-none bg-white"
                    >
                      <option value="mistral-large-latest">Mistral Large (Smartest)</option>
                      <option value="mistral-small-latest">Mistral Small (Fastest)</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={generateCaption}
                  disabled={loading || !thoughts}
                  className="w-full btn-primary flex items-center justify-center gap-2 group"
                >
                  {loading ? <Loader2 className="animate-spin" /> : <Sparkles className="group-hover:scale-125 transition-transform" size={20} />}
                  Generate Magic Caption
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Result Area */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="premium-card bg-linkedin-blue shadow-linkedin-blue/30 text-white p-6 md:p-10 relative overflow-hidden group"
            >
              <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-500">
                <Sparkles size={120} />
              </div>
              
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-extrabold flex items-center gap-2">
                    <Sparkles size={24} />
                    Magic Generated Content
                  </h3>
                  <button
                    onClick={handleCopy}
                    className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-all active:scale-95"
                  >
                    {copied ? <Check size={20} /> : <Copy size={20} />}
                  </button>
                </div>
                
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-lg leading-relaxed border border-white/20 whitespace-pre-wrap">
                  {result}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <footer className="mt-20 pb-8 text-slate-400 font-bold text-sm">
        © 2026 LinkedIn Magic Generator. Powered by Mistral AI.
      </footer>
    </main>
  );
}
