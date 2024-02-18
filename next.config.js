module.exports = {
    async rewrites() {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:5001/:path*' // Proxy to Backend
        }
      ]
    }
  }