import { Atividade } from '@/app/util/types';
import React from 'react';

export default function AtividadeCard({
    atividade,
    editavel,
    eliminavel,
    onEdit,
    onDelete,
}: {
    atividade: Atividade;
    editavel?: boolean;
    eliminavel?: boolean;
    onEdit?: () => void;
    onDelete?: () => void;
}) {
    return (
        <div className="border border-gray-300 p-6 rounded-2xl gap-2 flex flex-col">
            <h1>{atividade.descricao_atividade}</h1>
            <div className="w-full h-[1px] bg-gray-300"></div>
            <h2>
                {atividade.data_atividade} | {atividade.hora_atividade} |{' '}
                {atividade.localidade_atividade}
            </h2>
            <div className="w-full h-[1px] bg-gray-300"></div>
            <h2>{atividade.restricoes}</h2>

            {eliminavel && (
                <>
                    <div className="w-full h-[1px] bg-gray-300"></div>
                    <div className="flex items-center justify-center gap-4">
                        {editavel && (
                            <button
                                type="button"
                                onClick={onEdit}
                                className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                            >
                                Editar Atividade
                            </button>
                        )}
                        <button
                            type="button"
                            onClick={onDelete}
                            className="cursor-pointer transition duration-300 bg-red-500 hover:bg-red-900 text-white font-bold py-2 px-4 rounded mt-5"
                        >
                            Eliminar Atividade
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
