import React from 'react';
import { SyncLoader } from 'react-spinners';

export default function Loading() {
    return (
        <div className="flex flex-col items-center justify-center gap-2 absolute top-0 left-0 h-screen w-screen bg-white z-50 opacity-70">
            <SyncLoader />
            <p>Loading</p>
        </div>
    );
}
