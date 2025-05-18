import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

export default function Home() {
    return (
        <main className="grid grid-cols-[auto_1fr] min-h-[100dvh]">
            <Sidebar />
            <div>
                <Navbar />
            </div>
        </main>
    );
}
