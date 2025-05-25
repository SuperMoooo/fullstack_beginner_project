'use client';
import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import TitleInput from '../components/title_input';
import { Tipo } from '../util/types';
import Loading from '../components/loading';
import UpdateDataForm from './updateDataForm';
import DeleteAccountForm from './deleteAccountForm';

export default function Account() {
    const [nome, setNome] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [data_nascimento, setDataNascimento] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [tipo, setTipo] = useState<Tipo>('admin');
    const [nif, setNif] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [selectedIndex, setSelectedIndex] = useState<number>(0);
    const [deleteNome, setDeleteNome] = useState<string>('');
    const [deletePassword, setDeletePassword] = useState<string>('');
    const [confirmDeletePassword, setConfirmDeletePassword] =
        useState<string>('');
    const [deleteError, setDeleteError] = useState<string>('');

    useEffect(() => {
        getUserData();
    }, []);

    const getUserData = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const nome = localStorage.getItem('user_nome');
            const response = await fetch(
                `http://127.0.0.1:5000/get-user/${nome}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (response.ok) {
                const data = await response.json();
                setNome(data['nome']);
                setEmail(data['email']);
                setDataNascimento(data['data_nascimento']);
                setTipo(data['tipo']);
                setPassword(data['password']);
                if (data['tipo'] == 'user') {
                    setNif(data['nif']);
                }
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
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
    // ATUALIZAR
    const handleUpdateUserInfo = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            const token = localStorage.getItem('token');
            const user_nome = localStorage.getItem('user_nome');
            const response = await fetch(
                `http://127.0.0.1:5000/atualizar-user/${user_nome}`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        nome: nome,
                        email: email,
                        data_nascimento: data_nascimento,
                        password: password,
                        tipo: tipo,
                        nif: nif,
                    }),
                }
            );
            if (response.ok) {
                alert('Dados atualizados com sucesso!');
                localStorage.setItem('user_nome', nome);
                localStorage.setItem('tipo', tipo);
                setError('');
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
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

    // DELETE USER
    const handleDeleteUser = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            const token = localStorage.getItem('token');
            const user_nome = localStorage.getItem('user_nome');
            if (deletePassword !== confirmDeletePassword) {
                setDeleteError('As passwords não coincidem');
                return;
            }
            const response = await fetch(
                `http://127.0.0.1:5000/apagar-user/${user_nome}`,
                {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        nome: deleteNome,
                        password: deletePassword,
                    }),
                }
            );
            if (response.ok) {
                alert('Conta apagada com sucesso!');
                localStorage.removeItem('token');
                localStorage.removeItem('limite');
                localStorage.removeItem('user_nome');
                localStorage.removeItem('tipo');
                setDeleteError('');
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                setDeleteError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setDeleteError('Servidor Offline');
            } else {
                setDeleteError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar goBack={true} isConta={true} />
            <section className="flex items-center justify-start w-full px-20 pt-5 flex-col gap-4">
                {loading ? (
                    <Loading />
                ) : (
                    <>
                        <aside className="flex items-center justify-center gap-4 rounded-2xl p-4 bg-gray-100 border-gray-300 border *:cursor-pointer">
                            <p
                                onClick={() => setSelectedIndex(0)}
                                className={`${
                                    selectedIndex === 0
                                        ? 'text-blue-500 font-bold'
                                        : ''
                                }`}
                            >
                                Informações da conta
                            </p>
                            <p
                                onClick={() => setSelectedIndex(1)}
                                className={`${
                                    selectedIndex === 1
                                        ? 'text-blue-500 font-bold'
                                        : ''
                                }`}
                            >
                                Eliminar conta
                            </p>
                        </aside>
                        {selectedIndex === 0 ? (
                            <UpdateDataForm
                                handleUpdateUserInfo={handleUpdateUserInfo}
                                tipo={tipo}
                                setTipo={setTipo}
                                setNome={setNome}
                                setEmail={setEmail}
                                setDataNascimento={setDataNascimento}
                                setPassword={setPassword}
                                setNif={setNif}
                                nome={nome}
                                email={email}
                                data_nascimento={data_nascimento}
                                password={password}
                                nif={nif}
                                error={error}
                            />
                        ) : (
                            <DeleteAccountForm
                                handleDeleteUser={handleDeleteUser}
                                error={deleteError}
                                nome={deleteNome}
                                setNome={setDeleteNome}
                                password={deletePassword}
                                setPassword={setDeletePassword}
                                confirmPassword={confirmDeletePassword}
                                setConfirmPassword={setConfirmDeletePassword}
                            />
                        )}
                    </>
                )}
            </section>
        </main>
    );
}
