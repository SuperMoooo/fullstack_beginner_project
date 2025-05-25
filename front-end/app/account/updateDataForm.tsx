import React from 'react';
import { Tipo } from '../util/types';
import TitleInput from '../components/title_input';

export default function UpdateDataForm({
    handleUpdateUserInfo,
    tipo,
    setTipo,
    setNome,
    setEmail,
    setDataNascimento,
    setPassword,
    setNif,
    nome,
    email,
    data_nascimento,
    password,
    nif,
    error,
}: {
    handleUpdateUserInfo: (e: React.FormEvent<HTMLFormElement>) => void;
    tipo: Tipo;
    setTipo: any;
    setNome: any;
    setEmail: any;
    setDataNascimento: any;
    setPassword: any;
    setNif: any;
    nome: string;
    email: string;
    data_nascimento: string;
    password: string;
    nif: string;
    error: string;
}) {
    return (
        <form
            onSubmit={handleUpdateUserInfo}
            className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col w-2/4 p-10"
        >
            <div className="w-full flex items-start justify-between flex-col gap-2">
                <h1 className="text-lg">Tipo de Utilizador</h1>
                <select
                    defaultValue={tipo}
                    name="tipo"
                    id="tipo"
                    onChange={(e) => setTipo(e.target.value as Tipo)}
                    className="rounded-md border border-gray-300 bg-gray-100 p-2 outline-none w-full"
                >
                    <option value="admin">Admin</option>
                    <option value="user">Usuário</option>
                    <option value="participante">Participante</option>
                </select>
            </div>

            <TitleInput
                setValor={setNome}
                valor={nome}
                titulo="Nome"
                error={error.toLocaleLowerCase().includes('nome')}
            />
            <TitleInput
                setValor={setEmail}
                valor={email}
                titulo="Email"
                inputType="text"
                error={error.toLocaleLowerCase().includes('email')}
            />
            <TitleInput
                readOnly={true}
                setValor={setDataNascimento}
                valor={data_nascimento}
                titulo="Data de nascimento"
                error={error.toLocaleLowerCase().includes('data')}
            />
            <TitleInput
                setValor={setPassword}
                valor={password}
                titulo="Password"
                inputType="password"
                error={error.toLocaleLowerCase().includes('password')}
            />

            {tipo == 'user' && (
                <TitleInput
                    setValor={setNif}
                    valor={nif}
                    titulo="Nif"
                    error={error.toLocaleLowerCase().includes('nif')}
                />
            )}

            <button
                className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer hover:bg-blue-400"
                type="submit"
            >
                Atualizar Dados
            </button>
            {error && !error.includes('undefined') && (
                <p className="text-red-500">{error}</p>
            )}
        </form>
    );
}
