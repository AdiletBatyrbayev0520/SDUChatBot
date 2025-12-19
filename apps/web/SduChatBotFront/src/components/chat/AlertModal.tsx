import React from "react";

interface AlertModalProps {
    link: string;
    text: string;
    className?: string;
}

export const AlertModal = ({ link, text, className }: AlertModalProps) => {
    const [isOpen, setIsOpen] = React.useState(false);
    const [isVisible, setIsVisible] = React.useState(false);

    const openModal = (e: React.MouseEvent) => {
        e.preventDefault();
        setIsOpen(true);
        setTimeout(() => setIsVisible(true), 10);
    };

    const closeModal = () => {
        setIsVisible(false);
        setTimeout(() => setIsOpen(false), 200);
    };

    return (
        <>
            <a
                href={link}
                onClick={openModal}
                className={className + "cursor-pointer"}
            >
                {text}
            </a>


            {isOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    {/* Backdrop */}
                    <div
                        className={`absolute inset-0 bg-black/30 backdrop-blur-[2px] transition-opacity duration-300 ${
                            isVisible ? "opacity-100" : "opacity-0"
                        }`}
                        onClick={closeModal}
                    />

                    {/* Modal */}
                    <div
                        className={`relative w-full max-w-md px-6 py-5 bg-white  rounded-xl shadow-2xl transition-all duration-300 ${
                            isVisible
                                ? "opacity-100 translate-y-0"
                                : "opacity-0 translate-y-4"
                        }`}
                        style={{
                            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
                        }}
                    >
                        <div className="space-y-4">
                            <h3 className="text-xl font-semibold text-gray-900 ">
                                Внешняя ссылка
                            </h3>

                            <p className="text-gray-600 ">
                                Вы собираетесь перейти по внешней ссылке. Вы уверены, что хотите продолжить?
                            </p>

                            <div className="flex justify-end space-x-3 pt-2">
                                <button
                                    onClick={closeModal}
                                    className="px-4 py-2 text-sm font-medium text-gray-700  bg-gray-100  rounded-lg hover:bg-gray-200  transition-colors duration-200"
                                >
                                    Отмена
                                </button>
                                <a
                                    href={link}
                                    onClick={closeModal}
                                    className="px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors duration-200 flex items-center"
                                >
                                    Перейти
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="h-4 w-4 ml-1.5"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                                        />
                                    </svg>
                                </a>
                            </div>
                        </div>

                        <button
                            onClick={closeModal}
                            className="absolute top-4 right-4 p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 text-gray-500 "
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-5 w-5"
                                viewBox="0 0 20 20"
                                fill="currentColor"
                            >
                                <path
                                    fillRule="evenodd"
                                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                    clipRule="evenodd"
                                />
                            </svg>
                        </button>
                    </div>
                </div>
            )}
        </>
    );
};