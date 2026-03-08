import React from "react";

interface ResearchItem {
    id: string;
    title: string;
    url: string;
    published_at?: string;
    source?: string;
}

export default function ResearchList({ items }: { items: ResearchItem[] }) {
    if (!items || items.length === 0) {
        return <p>No research items found yet. The loop is still running!</p>;
    }

    return (
        <ul className="research-list">
            {items.map((item) => (
                <li key={item.id} className="research-item">
                    <a href={item.url} target="_blank" rel="noopener noreferrer">
                        {item.title}
                    </a>
                    <span className="source-tag">{item.source || "Unknown"}</span>
                </li>
            ))}
        </ul>
    );
}
