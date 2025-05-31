import React, { useState } from 'react';

export default function TitleInputFile({
    setValor,
    valor,
    error,
    accept,
}: {
    setValor: any;
    valor: File | null;
    inputType?: string;
    error?: boolean;
    accept?: string;
}) {
    return (
        <div className="flex items-start flex-col justify-center gap-2 w-full relative">
            <label
                htmlFor="fileInput"
                className={`flex items-center justify-center gap-4 flex-col rounded-md border  bg-gray-100 cursor-pointer outline-none w-full p-10  ${
                    error ? 'border-red-500' : 'border-gray-300'
                }`}
            >
                <h2>Selecione o arquivo</h2>
                {!valor ? (
                    <h4 className="text-6xl">+</h4>
                ) : (
                    <>
                        <img
                            src={
                                valor.type == 'application/vnd.ms-excel'
                                    ? 'csv_logo.png'
                                    : valor.type == 'application/pdf'
                                    ? 'pdf_logo.webp'
                                    : 'blank_file.png'
                            }
                            alt="file logo"
                            className="w-16 h-16"
                        />
                        <h2 className="text-center">{valor.name}</h2>
                    </>
                )}
            </label>
            <input
                id="fileInput"
                onChange={(e: any) => setValor(e.target.files[0])}
                type="file"
                accept={accept !== undefined ? accept : '.csv'}
                className="hidden"
            />
        </div>
    );
}
