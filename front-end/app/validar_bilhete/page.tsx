'use client';
import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

export default function ValidarBilhete() {
    return (
        <main className="grid grid-cols-[auto_1fr] min-h-[100dvh]">
            <Sidebar selected={2} />
            <div className="grid grid-rows-[auto_1fr]">
                <Navbar />
                <section className="flex items-center justify-center"></section>
            </div>
        </main>
    );
}
