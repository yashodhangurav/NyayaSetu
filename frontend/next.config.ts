import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "framerusercontent.com",
      },
    ],
  },
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async rewrites() {
    const backendUrl = process.env.BACKEND_API_URL || "http://127.0.0.1:8000";
    return [
      {
        source: "/models/lady-justice/source/model.glb",
        destination: "/models/lady-justice/model.glb",
      },
      {
        source: "/model/lady-justice-with-scales-and-sword/source/model.glb",
        destination: "/models/lady-justice/model.glb",
      },
      {
        source: "/model/lady-justice-with-scales-and-sword/textures/:name",
        destination: "/models/lady-justice/textures/:name",
      },
      {
        source: "/api/v1/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
