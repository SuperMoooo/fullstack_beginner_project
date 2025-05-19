import React from 'react';

export default function TitleInput({
    titulo,
    valor,
    setValor,
    inputType,
}: {
    titulo: string;
    valor: string;
    setValor: (valor: string) => void;
    inputType?: string;
}) {
    return (
        <div className="flex items-start flex-col justify-center gap-2">
            <h1 className="text-lg">{titulo}</h1>
            <input
                value={valor}
                onChange={(e) => setValor(e.target.value)}
                type={inputType ? inputType : 'text'}
                className="rounded-md border-2 bg-gray-100 p-2 outline-none"
            />
        </div>
    );
}
