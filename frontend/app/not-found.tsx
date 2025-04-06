import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-4xl font-bold text-gray-800 mb-4">404</h2>
      <p className="text-xl text-gray-600 mb-8">页面未找到</p>
      <Link href="/" className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition-colors">
        返回首页
      </Link>
    </div>
  );
} 