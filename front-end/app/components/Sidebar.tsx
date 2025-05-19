import Link from 'next/link';
import React from 'react';

export default function Sidebar({ selected }: { selected: number }) {
    return (
        <aside className="flex items-start justify-center gap-6 px-16 flex-col border-r border-gray-200 *:text-2xl *:flex *:items-center *:justify-center *:gap-2">
            <Link
                href={{ pathname: '/' }}
                className={selected == 0 ? 'underline' : ''}
            >
                <svg
                    aria-hidden="true"
                    fill="none"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-6 h-6"
                >
                    <path
                        d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                </svg>

                <p>Eventos</p>
            </Link>
            <Link
                href={{ pathname: '/pdfs' }}
                className={selected == 1 ? 'underline' : ''}
            >
                <svg
                    aria-hidden="true"
                    fill="none"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-6 h-6"
                >
                    <path
                        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                </svg>
                <p>PDF</p>
            </Link>
            <Link
                href={{ pathname: '/validar_bilhete' }}
                className={selected == 2 ? 'underline' : ''}
            >
                <svg
                    aria-hidden="true"
                    fill="none"
                    strokeWidth={1.5}
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-6 h-6"
                >
                    <path
                        d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 0 1 0 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 0 1 0-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375Z"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                </svg>
                <p>Validar Bilhete</p>
            </Link>
        </aside>
    );
}
