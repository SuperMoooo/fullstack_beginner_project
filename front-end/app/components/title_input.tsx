import React from 'react';

export default function TitleInput({
    titulo,
    valor,
    setValor,
    inputType,
    error,
}: {
    titulo: string;
    valor: string;
    setValor: (valor: string) => void;
    inputType?: string;
    error?: boolean;
}) {
    return (
        <div className="flex items-start flex-col justify-center gap-2 w-full">
            <h1 className="text-lg">{titulo}</h1>
            <input
                value={valor}
                onChange={(e) => setValor(e.target.value)}
                type={inputType ? inputType : 'text'}
                className={`rounded-md border  bg-gray-100 p-2 outline-none w-full ${
                    error ? 'border-red-500' : 'border-gray-300'
                }`}
            />
        </div>
    );
}
