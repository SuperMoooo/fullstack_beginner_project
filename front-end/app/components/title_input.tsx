import React, { useState } from 'react';

export default function TitleInput({
    titulo,
    valor,
    setValor,
    inputType,
    error,
    readOnly,
}: {
    titulo: string;
    valor: string;
    setValor: (valor: string) => void;
    inputType?: string;
    error?: boolean;
    readOnly?: boolean;
}) {
    const [showPassword, setShowPassword] = useState(false);
    return (
        <div className="flex items-start flex-col justify-center gap-2 w-full relative">
            <h1 className="text-lg">{titulo}</h1>
            <input
                readOnly={readOnly}
                value={valor}
                onChange={(e) => setValor(e.target.value)}
                type={showPassword ? 'text' : inputType ? inputType : 'text'}
                className={`rounded-md border  bg-gray-100 p-2 outline-none w-full ${
                    inputType == 'password' ? 'pr-10' : ''
                }  ${error ? 'border-red-500' : 'border-gray-300'}`}
            />

            {inputType == 'password' && (
                <div
                    className="absolute right-4 bottom-2.5 cursor-pointer"
                    onClick={() => setShowPassword(!showPassword)}
                >
                    {!showPassword ? (
                        <svg
                            aria-hidden="true"
                            fill="none"
                            strokeWidth={1.5}
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                            className="w-5 h-5"
                        >
                            <path
                                d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                            <path
                                d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                    ) : (
                        <svg
                            aria-hidden="true"
                            fill="none"
                            strokeWidth={1.5}
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                            className="w-5 h-5"
                        >
                            <path
                                d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                    )}
                </div>
            )}
        </div>
    );
}
