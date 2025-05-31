import React from 'react';
import { Tipo } from '../util/types';
import TitleInput from '../components/title_input';
import TitleSelect from '../components/title_select';

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
    sexo,
    setSexo,
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
    sexo: string;
    setSexo: any;
    error: string;
}) {
    return (
        <form
            onSubmit={handleUpdateUserInfo}
            className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col w-2/4 p-10"
        >
            <TitleSelect
                title="Tipo Utilizador"
                setValor={setTipo}
                valores={['Admin', 'Entreveniente', 'Participante']}
            />

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
            <TitleSelect
                title="Sexo"
                setValor={setSexo}
                valores={['Homem', 'Mulher', 'Outro', 'Prefiro não dizer']}
            />

            <TitleInput
                setValor={setNif}
                valor={nif}
                titulo="Nif"
                error={error.toLocaleLowerCase().includes('nif')}
            />

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
