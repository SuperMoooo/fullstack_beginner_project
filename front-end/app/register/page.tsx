'use client';
import Link from 'next/link';
import React, { useState } from 'react';
import Loading from '../components/loading';
import TitleInput from '../components/title_input';
import { Sexo, Tipo } from '../util/types';
import TitleSelect from '../components/title_select';

export default function RegisterPage() {
    const [nome, setNome] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [data_nascimento, setDataNascimento] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [tipo, setTipo] = useState<Tipo>('Admin');
    const [sexo, setSexo] = useState<Sexo>('Homem');
    const [nif, setNif] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    // HANDLE REGISTER
    const register = async (e: any) => {
        try {
            e.preventDefault();
            let day = data_nascimento.split('-')[2];
            let month = data_nascimento.split('-')[1].split('-')[0];
            let year = data_nascimento.split('-')[0];
            const birthDate = `${day}/${month}/${year}`;

            setLoading(true);
            if (nome == '' || password == '' || email == '') {
                alert('Preencha todos os campos!');
                setError('Preencha todos os campos!');
                return;
            }
            let response;

            response = await fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nome: nome,
                    email: email,
                    data_nascimento: birthDate,
                    sexo: sexo,
                    nif: nif,
                    password: password,
                    tipo: tipo,
                }),
            });

            // SALVAR TOKEN E LIMITE
            if (response.ok) {
                alert('Sucesso');
                setError('');
                window.location.href = '/login';
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] || 'Erro desconhecido');
                alert(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] h-[100dvh]">
            <header className="flex justify-start items-center py-4 px-20 border-b border-gray-300">
                <Link
                    href={{ pathname: '/login' }}
                    className="text-2xl cursor-pointer"
                >
                    &#60; Voltar
                </Link>
            </header>
            <section className="flex items-center justify-center ">
                <form
                    className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10 w-1/3"
                    onSubmit={register}
                >
                    <h1 className="text-3xl">Criar conta</h1>
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
                        setValor={setDataNascimento}
                        valor={data_nascimento}
                        titulo="Data de nascimento"
                        inputType="date"
                        error={error.toLocaleLowerCase().includes('data')}
                    />
                    <TitleSelect
                        title="Sexo"
                        setValor={setSexo}
                        valores={[
                            'Homem',
                            'Mulher',
                            'Outro',
                            'Prefiro não dizer',
                        ]}
                    />

                    <TitleInput
                        setValor={setNif}
                        valor={nif}
                        titulo="Nif"
                        error={error.toLocaleLowerCase().includes('nif')}
                    />

                    <TitleInput
                        setValor={setPassword}
                        valor={password}
                        titulo="Password"
                        inputType="password"
                        error={error.toLocaleLowerCase().includes('password')}
                    />

                    <button
                        className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer hover:bg-blue-400"
                        type="submit"
                    >
                        Entrar
                    </button>
                    {error && !error.includes('undefined') && (
                        <p className="text-red-500">{error}</p>
                    )}
                    <h3>
                        Já tem conta?{' '}
                        <Link
                            href={{ pathname: '/login' }}
                            className="underline text-blue-700"
                        >
                            Entrar!
                        </Link>
                    </h3>
                </form>
                {loading && <Loading />}
            </section>
        </main>
    );
}
