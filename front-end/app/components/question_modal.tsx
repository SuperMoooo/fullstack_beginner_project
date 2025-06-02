import React from 'react';

export default function QuestionModal({
    title,
    message,
    onConfirm,
    onCancel,
    show,
}: {
    title: string;
    message: string;
    onConfirm: any;
    onCancel: () => void;
    show: boolean;
}) {
    return (
        <main
            className={`fixed flex items-center justify-center h-screen w-screen bg-black/50 ${
                show ? 'flex' : 'hidden'
            }`}
        >
            <section className="w-fit flex flex-col gap-2 items-center justify-center *:text-center bg-white rounded-2xl p-6">
                <h1 className="text-2xl">{title}</h1>
                <h2 className="text-lg">{message}</h2>
                <div className="flex items-center justify-center gap-4">
                    <button
                        onClick={onCancel}
                        className="cursor-pointer transition duration-300 bg-gray-500 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded mt-5"
                    >
                        Cancelar
                    </button>
                    <button
                        onClick={onConfirm}
                        className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5"
                    >
                        Confirmar
                    </button>
                </div>
            </section>
        </main>
    );
}
