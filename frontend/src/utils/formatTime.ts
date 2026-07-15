export function formatRelativeTime(dateString: string): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return 'Just now';
  } else if (diffInSeconds < 3600) {
    const min = Math.floor(diffInSeconds / 60);
    return `${min} min ago`;
  } else if (diffInSeconds < 86400) {
    const hr = Math.floor(diffInSeconds / 3600);
    return `${hr} hr ago`;
  } else if (diffInSeconds < 172800) {
    return 'Yesterday';
  } else {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days} days ago`;
  }
}
