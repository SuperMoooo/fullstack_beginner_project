import React from 'react';

export default function TitleSelect({
    title,
    setValor,
    valores,
}: {
    title: string;
    setValor: any;
    valores: string[];
}) {
    return (
        <div className="w-full flex items-start justify-between flex-col gap-2">
            <h1 className="text-lg">{title}</h1>
            <select
                name="tipo"
                id="tipo"
                onChange={(e) => setValor(e.target.value)}
                className="rounded-md border border-gray-300 bg-gray-100 p-2 outline-none w-full"
            >
                {valores.map((valor, index) => (
                    <option key={index} value={valor}>
                        {valor}
                    </option>
                ))}
            </select>
        </div>
    );
}
