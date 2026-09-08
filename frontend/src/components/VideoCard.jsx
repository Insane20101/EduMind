import React from 'react';
import { PlayCircle, Tv, ExternalLink } from 'lucide-react';

export default function VideoCard({ item, onClick }) {
  let embedUrl = null;
  const url = item.url;
  
  try {
    if (url && typeof url === 'string') {
      if (url.includes('list=')) {
        const listId = new URL(url).searchParams.get('list');
        if (listId) embedUrl = `https://www.youtube.com/embed/videoseries?list=${listId}`;
      } else if (url.includes('watch?v=')) {
        const videoId = new URL(url).searchParams.get('v');
        if (videoId) embedUrl = `https://www.youtube.com/embed/${videoId}`;
      }
    }
  } catch(e) {}

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl border border-border-subtle shadow-sm overflow-hidden hover:shadow-lg transition-all group flex flex-col h-full cursor-pointer hover:-translate-y-0.5"
    >
      <div className="aspect-video w-full bg-black relative flex items-center justify-center group overflow-hidden">
        <div className="absolute inset-0 bg-black group-hover:bg-slate-950 transition-colors z-10" />
        
        <div className="z-20 p-3 rounded-full bg-indigo-600/90 text-white shadow-xl group-hover:scale-110 group-hover:bg-indigo-600 transition-all">
          <PlayCircle size={36} className="fill-current text-white" />
        </div>

        <div className="absolute bottom-2 right-2 bg-black/80 backdrop-blur-sm text-white text-[11px] font-medium px-2 py-0.5 rounded-md z-20 flex items-center gap-1">
          <Tv size={12} className="text-indigo-400" />
          <span>{item.unit || 'Playlist'}</span>
        </div>
      </div>
      
      <div className="p-4 flex-grow flex flex-col justify-between">
        <div>
          <h4 className="font-semibold text-text-primary line-clamp-2 mb-1 group-hover:text-indigo-600 transition-colors" title={item.title}>
            {item.title}
          </h4>
          <p className="text-xs text-text-secondary line-clamp-1">
            {item.channel || 'Complete Lecture Course'}
          </p>
        </div>

        <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-indigo-600">
          <span>Watch Theater View</span>
          <ExternalLink size={14} />
        </div>
      </div>
    </div>
  );
}

