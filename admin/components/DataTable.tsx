import Card from './Card'

type User = { id: string; email: string; is_superuser: boolean; created_at: string }

export default function DataTable({ data }: { data: User[] }) {
  return (
    <Card>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="text-left opacity-70">
            <tr>
              <th className="py-2 pr-4">Email</th>
              <th className="py-2 pr-4">Admin</th>
              <th className="py-2 pr-4">Created</th>
            </tr>
          </thead>
          <tbody>
            {data.length === 0 && (
              <tr><td className="py-4" colSpan={3}>No users yet</td></tr>
            )}
            {data.map(u => (
              <tr key={u.id} className="border-t border-white/10">
                <td className="py-2 pr-4">{u.email}</td>
                <td className="py-2 pr-4">{u.is_superuser ? 'Yes' : 'No'}</td>
                <td className="py-2 pr-4">{new Date(u.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}


