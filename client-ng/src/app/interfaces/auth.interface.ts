export interface LoginProps {
    code: string;
    password: string;
};

export interface RegisterProps {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    dni: string;
    password: string;
    password2: string;
};

interface FacultadProps {
    id: number;
    name: string;
};

interface ProgAcadProps {
    id: number;
    name: string;
    facultad: FacultadProps;
};

export interface GetUserProps {
    code: string;
    email: string;
    first_name: string;
    last_name: string;
    prog_acad: ProgAcadProps;
};