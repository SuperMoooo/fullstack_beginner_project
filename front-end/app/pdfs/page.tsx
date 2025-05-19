import Navbar from './../components/Navbar';
import Sidebar from './../components/Sidebar';

export default function Pdfs() {
    return (
        <main className="grid grid-cols-[auto_1fr] min-h-[100dvh]">
            <Sidebar selected={1} />
            <div>
                <Navbar />
            </div>
        </main>
    );
}
