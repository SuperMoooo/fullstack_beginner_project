import React from 'react';

export default function TitleMicInput({
    titulo,
    error,
    handleCaptureAudio,
    valor,
    setValor,
    micActive,
}: {
    titulo: string;
    error?: boolean;
    handleCaptureAudio: () => void;
    valor: string;
    setValor: any;
    micActive: boolean;
}) {
    return (
        <div className="flex items-center justify-center flex-col gap-4 relative w-full ">
            <h1 className="text-lg self-start">{titulo}</h1>
            <input
                onChange={(e) => setValor(e.target.value)}
                value={valor}
                type="text"
                className={`rounded-md border  bg-gray-100 p-2 outline-none w-full  ${
                    error ? 'border-red-500' : 'border-gray-300'
                }`}
            />
            <div
                className="absolute right-4 bottom-2.5 cursor-pointer"
                onClick={handleCaptureAudio}
            >
                <svg
                    aria-hidden="true"
                    fill="none"
                    strokeWidth={1.5}
                    stroke={micActive ? 'red' : 'currentColor'}
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-6 h-6"
                >
                    <path
                        d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                </svg>
            </div>
        </div>
    );
}
