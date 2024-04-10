/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
          {
            source: '/log/individual',
            destination: 'http://127.0.0.1:5000/log/individual', // Proxy to Backend
          },
        ]
    },
};

export default nextConfig;
