type Props = {
  status?: string | null;
};

export default function ReportStatusBadge({ status }: Props) {
  const normalized = (status || "reported").toLowerCase();

  const styles: Record<string, string> = {
    reported: "bg-blue-100 text-blue-800",
    pending: "bg-yellow-100 text-yellow-800",
    assigned: "bg-purple-100 text-purple-800",
    in_progress: "bg-orange-100 text-orange-800",
    repaired: "bg-green-100 text-green-800",
    completed: "bg-green-100 text-green-800",
    rejected: "bg-red-100 text-red-800",
  };

  const label = normalized.replace(/_/g, " ");

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold capitalize ${
        styles[normalized] || "bg-gray-100 text-gray-800"
      }`}
    >
      {label}
    </span>
  );
}