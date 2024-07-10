import {
  NavigationMenu,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import { useToken } from "@/providers/token.provider";
import { ModeToggle } from "../main/mode_toggle";

const Navbar = () => {
  const { key, setKey } = useToken();

  async function logout() {
    setKey(null);
  }

  return (
    <>
      <nav>
        <div className="w-full h-12 sm:h-14 bg-gray-400 flex justify-between items-center px-4 sm:px-6">
          <div className="text-sm sm:text-md lg:text-xl font-semibold text-transform: capitalize">
            Gestión de Tesis
          </div>
          {key ? (
            <NavigationMenu className="text-center text-sm sm:text-md lg:text-lg font-semibold rounded-2xl bg-none ">
              <NavigationMenuList>
                <button>
                  <div
                    className="hover:bg-cyan-500 rounded-md cursor-pointer"
                    onClick={logout}
                  >
                    <NavigationMenuLink className="bg-none pr-2 flex items-center">
                      <span className="pl-2">Cerrar sesión</span>
                    </NavigationMenuLink>
                  </div>
                </button>
                <ModeToggle />
              </NavigationMenuList>
            </NavigationMenu>
          ) : (
            <ModeToggle />
          )}
        </div>
      </nav>
    </>
  );
};

export default Navbar;
