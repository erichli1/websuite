/** @type {import('next').NextConfig} */

import pkg from '@next/env';
const { loadEnvConfig } = pkg

const projectDir = process.cwd();
loadEnvConfig(projectDir);

const nextConfig = {
    async rewrites() {
        return [
          {
            source: '/log/individual',
            destination: `http://127.0.0.1:${process.env.FLASK_RUN_PORT}/log/individual`,
          },
        ]
    },
};

export default nextConfig;
