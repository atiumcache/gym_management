import { Outlet } from 'react-router'

export function Dashboard() {
    return (
        <div>
            <h1>Dashboard...</h1>
            <Outlet />
        </div>
    )
}