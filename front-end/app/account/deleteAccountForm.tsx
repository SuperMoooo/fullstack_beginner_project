import React from 'react';
import TitleInput from '../components/title_input';

export default function DeleteAccountForm({
    handleDeleteUser,
    error,
    nome,
    setNome,
    password,
    setPassword,
    confirmPassword,
    setConfirmPassword,
}: {
    handleDeleteUser: (e: React.FormEvent<HTMLFormElement>) => void;
    error: string;
    nome: string;
    setNome: any;
    password: string;
    setPassword: any;
    confirmPassword: string;
    setConfirmPassword: any;
}) {
    return (
        <form
            onSubmit={handleDeleteUser}
            className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col w-2/4 p-10"
        >
            <TitleInput
                setValor={setNome}
                valor={nome}
                titulo="Seu Nome"
                error={error.toLocaleLowerCase().includes('nome')}
            />
            <TitleInput
                setValor={setPassword}
                valor={password}
                titulo="Sua Password"
                inputType="password"
                error={error.toLocaleLowerCase().includes('password')}
            />
            <TitleInput
                setValor={setConfirmPassword}
                valor={confirmPassword}
                titulo="Confirmar Password"
                inputType="password"
                error={error.toLocaleLowerCase().includes('password')}
            />
            <button
                className="border rounded-2xl text-white bg-red-500 p-4 w-full cursor-pointer hover:bg-red-400"
                type="submit"
            >
                Eliminar Conta
            </button>
            {error && !error.includes('undefined') && (
                <p className="text-red-500">{error}</p>
            )}
        </form>
    );
}
