import random
from typing import *

__all__ = ['Atom', 'bond', 'delete_atom', 'get_all_atoms', 'get_atom', 'get_atom_id', 'reset_tags']


class Atom:
    """
    The Atom class is used to represent an atom in a structure, containing its elements, charge, lone pair electrons,
    chemical bonds, and unique ID. It also includes some methods to achieve functions such as atomic bonding, breaking
    bonds, and modifying atomic parameters.

    Attributes:
        element_info (dict[str, list]): Basic information of elements. (Class attribute)
        id_map (dict[int, Atom]): The mapping relationship between IDs and registered Atom instances. (Class attribute)
        id_pool (List[int]): Available IDs. (Class attribute)

        access_tag (bool): A tag used during traversing the structure.
        bonds (List[int] | None): Record the atoms bonded to the current atom.
        charge (int): The charge number of the current atom.
        element (str): The element of the current atom.
        id (int): A unique ID identifies an atom.
        lone_electron (int): The number of lone electrons in the current atom.

    Raises:
        AtomError
        BondError
        ChargeError
        ElementError
        IdError
        LoneElectronError
    """
    __slots__ = ('access_tag', 'bonds', 'charge', 'element', 'id', 'lone_electron')
    element_info: Dict[str, List[any]] = {"C": [4, 8], "H": [1, 2], "O": [6, 8], "N": [5, 8],
                                          "S": [6, 8], "P": [5, 8], "Cl": [7, 8], "Br": [7, 8],
                                          "I": [7, 8]}
    id_map: Dict[int, 'Atom'] = {}
    id_pool: List[int] = list(range(1000, 10000, 1))
    access_tag: bool
    bonds: Optional[List[int]]
    charge: int
    element: str
    id: int
    lone_electron: int

    def __init__(self, element: str = "H", bonds: Optional[List[Union[int, 'Atom']]] = None,
                 charge: int = 0, lone_electron: Optional[int] = None, bond_: bool = True,
                 auto_modify: bool = False) -> None:
        """
        Initialize class Atom.

        Args:
            element (str): The element of the atom. Default to "H".
            bonds (list[int | Atom] | None): The atoms bonded to the atom. Default to None.
            charge (int): The charge number of the atom. Default to 0.
            lone_electron (int | None): The number of lone electrons in the atom. Default to None (automatically set).
            bond_ (bool): Whether to automatically bond with atoms in bonds. Default to True. (Warning: do not set this
                          parameter to False. Otherwise, it will lead to some unexpected problems)
            auto_modify (bool): Whether to automatically adjust the number of lone electrons. Default to False.

        Raises:
            AtomError
            BondError
            ChargeError
            ElementError
            IdError
            LoneElectronError
        """
        if bonds is None:
            bonds = []
        self.element = element
        self.charge = charge
        self.lone_electron = 0 if lone_electron is None else lone_electron
        self.id = Atom.__generate_id()
        for i, atom in enumerate(bonds):
            bonds[i] = Atom.get_atom_id(atom)
        self.bonds = bonds
        n, self.lone_electron = Atom.__bond_num(self.element, charge, self.lone_electron, bonds,
                                                self.id, True if lone_electron is None else auto_modify)
        Atom.id_map[self.id] = self
        for i, atom in enumerate(self.bonds):
            if bond_:
                try:
                    Atom.get_atom(atom).bond_with(self, bond_back=False)
                except Exception as a:
                    self.bonds.pop(i)
                    raise a
        while len(self.bonds) < n:
            hydro = Atom(bonds=[self.id], bond_=False)
            self.bonds.append(hydro.get_id())
        self.access_tag = False

    def __str__(self) -> str:
        self.survive()
        bonds = "["
        for i in self.get_bonds():
            bonds += str(i) + "(" + Atom.get_atom(i).get_element() + "), "
        bonds = bonds[:-2] + "]"
        return f"<Atom id={self.get_id()}, element={self.get_element()}, bonds={bonds}, " \
               + f"charge={self.get_charge()}, lone_electron={self.get_lone_electron()}>"

    def __repr__(self) -> str:
        self.survive()
        bonds = "["
        for i in self.get_bonds():
            bonds += str(i) + "(" + Atom.get_atom(i).get_element() + "), "
        bonds = bonds[:-2] + "]"
        return f"<Atom id={self.get_id()}, element={self.get_element()}, bonds={bonds}, " \
               + f"charge={self.get_charge()}, lone_electron={self.get_lone_electron()}>"

    @classmethod
    def __generate_id(cls) -> int:
        if len(Atom.id_pool) == 0:
            raise IdError("[Id Pool Runs Out] Failed to generate a new id. " +
                          f"You can only register 9000 atoms at the same time.", )
        return cls.id_pool.pop(random.randint(0, len(Atom.id_pool) - 1))

    @classmethod
    def __bond_num(cls, element: str, charge: int, lone_electron: int,
                   existing_bond: Optional[List[int]] = None, id_: int = 0,
                   auto_modify: bool = False) -> Tuple[int, int]:
        if lone_electron < 0:
            raise LoneElectronError(
                f"[Atom {id_}] The number of lone electrons must be non-negative.", id_)
        if existing_bond is None:
            existing_bond = []
        bonds_ = existing_bond.copy()
        d = 0
        while len(bonds_) > 0:
            i = bonds_[0]
            if bonds_.count(i) == 2:
                d += 1
            while i in bonds_:
                bonds_.remove(i)
        existing_bond = len(existing_bond)
        info = cls.element_info.get(element, None)
        if info is None:
            Atom.id_pool.append(id_)
            raise ElementError(
                f"[Atom {id_}] Element '{element}' not found. " +
                f"This element may not exist or it is currently not supported.",
                id_)
        n = info[0] - charge
        if n < 0:
            Atom.id_pool.append(id_)
            raise ChargeError(
                f"[Atom {id_}] No enough valence electrons for the +{charge} " +
                f"valence state (The maximum supported positive charge is +{info[0]}).",
                id_)
        if n > info[1]:
            Atom.id_pool.append(id_)
            raise ChargeError(
                f"[Atom {id_}] No enough empty orbitals for the {charge} " +
                f"valence state (The maximum supported negative charge is -{info[1] - info[0]}).",
                id_)
        if n - existing_bond < 0:
            Atom.id_pool.append(id_)
            raise BondError(
                f"[Atom {id_}] Too many Bonds (Only {n} bonds can be formed, but there exist {existing_bond} bonds)."
                    .replace("exist 1 bonds", "exists 1 bond")
                    .replace("1 bonds", "1 bond"), id_)
        if n - existing_bond < lone_electron:
            Atom.id_pool.append(id_)
            raise ChargeError(
                f"[Atom {id_}] No enough valence electrons for {lone_electron} " +
                f"lone electrons (There are {n} remaining valence electrons available)."
                .replace("1 lone electrons", "1 lone electron")
                .replace("1 remaining valence electrons", "1 remaining valence electron"), id_)
        n = n - lone_electron
        if lone_electron + 2 * n > info[1]:
            lone_electron_ = lone_electron
            n_ = n
            while lone_electron_ + 2 * n_ - 2 * d > info[1] and n_ > existing_bond:
                lone_electron_ += 1
                n_ -= 1
            if not auto_modify and lone_electron != lone_electron_:
                raise LoneElectronError(
                    f"[Atom {id_}] {lone_electron_} lone electrons are needed instead of {lone_electron}. "
                    .replace("1 lone electrons", "1 lone electron") +
                    f"To automatically modify to the appropriate number of lone electrons, " +
                    "please add \'auto_modify = True\'.", id_)
            else:
                if lone_electron_ + 2 * n_ - 2 * d > info[1]:
                    raise BondError(
                        f"[Atom {id_}] {lone_electron_} Too many Bonds. These bonds need " +
                        f"{100 - (200 - (lone_electron_ + 2 * n_ - 2 * d)) // 2} " +
                        f"molecular orbitals but only {info[1] / 2} are available.",
                        id_)
                lone_electron, n = lone_electron_, n_
        return n, lone_electron

    @classmethod
    def __remove_hydro(cls, bonds: List[int]) -> List[int]:
        bonds_ = []
        for i in bonds:
            if get_atom(i).get_element() != "H":
                bonds_.append(i)
        return bonds_

    @classmethod
    def bond(cls, atom_1: Union[int, 'Atom'], atom_2: Union[int, 'Atom'],
             use: Literal['hydro', 'lone_electron', 'all'] = "hydro", allow_carbene: bool = False) -> None:
        """
        Bond two atoms through hydrogen atoms, lone electrons, or both.

        Args:
            atom_1 (int | Atom): The first atom for bonding.
            atom_2 (int | Atom): The second atom for bonding.
            use (Literal['hydro', 'lone_electron', 'both']): If use == "hydro", it means each of the two atoms loses a
                                                             hydrogen atom to form a bond (default). If use ==
                                                             "lone_electron", it means use lone electrons on the two
                                                             atoms to form bonds if possible. If use == "both", it means
                                                             use both.
            allow_carbene (bool): Whether to allow losing two hydrogen atoms on the same atom to form a carbene-like
                                  structure. Default to False.

        Raises:
            AtomError
            BondError
            LoneElectronError
        """
        Atom.get_atom(atom_1).bond_with(Atom.get_atom(atom_2), use=use, allow_carbene=allow_carbene)

    @classmethod
    def break_bond(cls, atom_1: Union[int, 'Atom'], atom_2: Union[int, 'Atom']) -> None:
        """
        Break a bond between two atoms.

        Args:
            atom_1 (int | Atom): The first atom for breaking bond.
            atom_2 (int | Atom): The second atom for breaking bond.

        Raises:
            AtomError
            BondError
        """
        Atom.get_atom(atom_1).break_bond_with(Atom.get_atom(atom_2))

    @classmethod
    def delete_atom(cls, atom: Union[int, 'Atom']) -> None:
        """
        Delete the current atom, Remove it from the list of registered atoms.

        Raises:
            AtomError
        """
        Atom.get_atom(atom).delete()

    @classmethod
    def get_all_atoms(cls) -> List['Atom']:
        """
        Get the list of registered atoms.

        Returns:
            list['Atom']: The list of registered atoms.
        """
        return list(cls.id_map.values())

    @classmethod
    def get_atom(cls, atom: Union[int, 'Atom']) -> 'Atom':
        """
        Get an Atom instance through id or instance.

        Args:
            atom (int | Atom): An id or an instance represents the atom.

        Returns:
            Atom: The instance represents the atom.

        Raises:
            AtomError
        """
        if type(atom) == Atom:
            atom.survive()
            return atom
        elif type(atom) == int:
            ret = cls.id_map.get(atom, None)
            if ret is None:
                raise AtomError(
                    f"[Non-existent Atom {atom}] Atom {atom} does not exist.", atom)
            return ret
        else:
            raise AtomError(
                f"[Non-existent Atom {repr(atom)}] Please use an Atom object or an id to represent an atom.", atom)

    @classmethod
    def get_atom_id(cls, atom: Union[int, 'Atom']) -> int:
        """
        Get the id of an Atom instance through id or instance.

        Args:
            atom (int | Atom): An id or an instance represents the atom.

        Returns:
            Atom: The id represents the atom.

        Raises:
            AtomError
        """
        if type(atom) == Atom:
            atom.survive()
            return atom.get_id()
        elif type(atom) == int:
            ret = cls.id_map.get(atom, None)
            if ret is None:
                raise AtomError(
                    f"[Non-existent Atom {atom}] Atom {atom} does not exist.", atom)
            return atom
        else:
            raise AtomError(
                f"[Non-existent Atom {repr(atom)}] Please use an Atom object or an id to represent an atom.", atom)

    @classmethod
    def reset_tags(cls) -> None:
        """
        Set all the access tags to False.
        """
        for i in cls.id_map.values():
            i.access_tag = False

    def bond_with(self, atom: Union[int, 'Atom'], bond_back: bool = True,
                  use: Literal['hydro', 'lone_electron', 'both'] = "hydro", allow_carbene: bool = False) -> None:
        """
        Bond the current atom with another atom through hydrogen atoms, lone electrons, or both.

        Args:
            atom (int | Atom): Target atom for bonding.
            bond_back (bool): Whether to bond back. Default to True. (Warning: do not set this parameter to False.
                              Otherwise, it will lead to some unexpected problems)
            use (Literal['hydro', 'lone_electron', 'both']): If use == "hydro", it means each of the two atoms loses a
                                                             hydrogen atom to form a bond (default). If use ==
                                                             "lone_electron", it means use lone electrons on the two
                                                             atoms to form bonds if possible. If use == "both", it means
                                                             use both.
            allow_carbene (bool): Whether to allow losing two hydrogen atoms on the same atom to form a carbene-like
                                  structure. Default to False.

        Raises:
            AtomError
            BondError
            LoneElectronError
        """
        self.survive()
        if use == "lone_electron" and allow_carbene:
            raise LoneElectronError(
                f"[Atom {self.get_id()}] To use \'allow_carbene = True\',"
                + f"please do not set \'use = \"lone_electron\"\'.",
                self.get_id())
        bondable = False
        if Atom.get_atom(atom) is self:
            if allow_carbene:
                h = []
                for i, a in enumerate(self.get_bonds()):
                    if Atom.get_atom(a).get_element() == "H":
                        h.append((i, a))
                        if len(h) == 2:
                            bondable = True
                            break
                if not bondable:
                    raise LoneElectronError(
                        f"[Atom {self.get_id()}] No enough electron available to " +
                        "form a carbene-like structure ({len(h)} are available while 2 are needed)."
                        .replace("1 are", "1 is"), self.get_id())
                self.get_lone_electron += 2
                self.get_bonds().pop(h[0][0])
                Atom.get_atom(h[0][1]).delete()
                self.get_bonds().pop(h[1][0])
                Atom.get_atom(h[1][1]).delete()
            else:
                raise BondError(
                    f"[Atom {self.get_id()}] An atom cannot bond with itself. " +
                    f"Are you trying to form a carbene-like structure? If so, please add \'allow_carbene = True\'.",
                    self.get_id())
        else:
            ex = None
            if use == "lone_electron" or use == "both":
                try:
                    n, lone_electron_ = Atom.__bond_num(self.get_element(), self.get_charge(),
                                                        self.get_lone_electron() - 1, self.get_bonds(), self.get_id())
                    if n == n + 1:
                        self.lone_electron = lone_electron_
                        self.get_bonds().append(Atom.get_atom_id(atom))
                        bondable = True
                except Exception as e:
                    ex = e
            for i, a in enumerate(self.get_bonds()):
                if Atom.get_atom(a).get_element() == "H" and (use == "hydro" or use == "both"):
                    Atom.get_atom(a).delete()
                    self.get_bonds()[i] = Atom.get_atom_id(atom)
                    bondable = True
                    break
            if not bondable:
                raise BondError(
                    f"[Atom {self.get_id()}] Too many Bonds (You are trying to add 1 more bond, " +
                    f"but there already exist {len(self.get_bonds())} bonds and it's impossible to form a new bond)."
                    .replace("exist 1 bonds", "exists 1 bond") +
                    (
                        " Add \'use = \"lone_electron\"\' to use lone electron to form a bond, "
                        if use == "hydro" else "") +
                    (
                        " Add \'use = \"hydro\"\' to use hydrogen atom to form a bond, "
                        if use == "lone_electron" else "") +
                    ("" if use == "both" else "or add \'use = \"both\"\' to use both hydrogen atom and lone electron."),
                    self.get_id())from ex
            if bond_back:
                Atom.get_atom(atom).bond_with(self, bond_back=False)

    def break_bond_with(self, atom: Union[int, 'Atom'], break_bond_back: bool = True) -> None:
        """
        Break a bond between the current atom and another atom.

        Args:
            atom (int | Atom): Target atom for breaking bond.
            break_bond_back (bool): Whether to break bond back. Default to True. (Warning: do not set this parameter to
                                    False. Otherwise, it will lead to some unexpected problems)

        Raises:
            AtomError
            BondError
        """
        self.survive()
        atom = Atom.get_atom_id(atom)
        find_ = False
        for i in self.get_bonds():
            if atom == i:
                find_ = True
                break
        if not find_:
            raise BondError(
                f"[Atom {self.get_id()}] You are trying to break a bond with atom {atom}, but the bond does not exit.",
                self.get_id())
        self.bonds.remove(atom)
        self.set_lone_electron(self.get_lone_electron() + 1)
        if break_bond_back:
            Atom.get_atom(atom).break_bond_with(self, break_bond_back=False)

    def delete(self) -> None:
        """
        Delete the current atom, Remove it from the list of registered atoms.

        Raises:
            AtomError
        """
        self.survive()
        Atom.id_pool.append(self.get_id())
        Atom.id_map.pop(self.get_id())
        del self

    def get_bonds(self) -> List[int]:
        """
        Get the bonds attribute.

        Returns:
            list[int]: A list records the atoms bonded to the current atom.

        Raises:
            AtomError
        """
        self.survive()
        return self.bonds

    def get_charge(self) -> int:
        """
        Get the charge attribute.

        Returns:
            int: The charge number of the current atom.

        Raises:
            AtomError
        """
        self.survive()
        return self.charge

    def get_element(self) -> str:
        """
        Get the element attribute.

        Returns:
            int: The element of the current atom.

        Raises:
            AtomError
        """
        self.survive()
        return self.element

    def get_id(self) -> int:
        """
        Get the id attribute.

        Returns:
            int: The ID of the current atom.

        Raises:
            AtomError
        """
        self.survive()
        return self.id

    def get_lone_electron(self) -> int:
        """
        Get the lone_electron attribute.

        Returns:
            The number of lone electrons in the current atom.

        Raises:
            AtomError
        """
        self.survive()
        return self.lone_electron

    def set_charge(self, charge: int) -> None:
        """
        Set the charge attribute to a new number.

        Args:
            charge (int): new charge number you want to assign to the charge attribute.

        Raises:
            AtomError
            BondError
            ChargeError
        """
        self.survive()
        n, lone_electron = Atom.__bond_num(self.get_element(), charge,
                                           self.get_lone_electron(), Atom.__remove_hydro(self.get_bonds()),
                                           self.get_id())
        self.charge = charge
        while n > len(self.get_bonds()):
            hydro = Atom(bonds=[self.id], bond_=False)
            self.bonds.append(hydro.get_id())
        if n < len(self.get_bonds()):
            count_h = 0
            h = []
            for i, a in enumerate(self.get_bonds()):
                if Atom.get_atom(a).get_element() == "H":
                    count_h += 1
                    h.append(i)
            if count_h < len(self.get_bonds()) - n:
                raise ChargeError(
                    f"[Atom {self.get_id()}] Failed to set +{charge} charge. ".replace("+-", "-") +
                    f"There are too many bonds that cannot be removed.", self.get_id())
            j = 0
            while n < len(self.get_bonds()):
                i = h.pop(0)
                self.bonds.pop(i - j)
                j += 1

    def set_element(self, element: str) -> None:
        """
        Set the element attribute to a new number.

        Args:
            element (int): new element you want to assign to the element attribute.

        Raises:
            AtomError
            BondError
            ElementError
        """
        self.survive()
        n, lone_electron = Atom.__bond_num(element, self.get_charge(),
                                           self.get_lone_electron(), Atom.__remove_hydro(self.get_bonds()),
                                           self.get_id())
        self.element = element
        while n > len(self.get_bonds()):
            hydro = Atom(bonds=[self.id], bond_=False)
            self.bonds.append(hydro.get_id())
        if n < len(self.get_bonds()):
            count_h = 0
            h = []
            for i, a in enumerate(self.get_bonds()):
                if Atom.get_atom(a).get_element() == "H":
                    count_h += 1
                    h.append(i)
            if count_h < len(self.get_bonds()) - n:
                raise ElementError(
                    f"[Atom {self.get_id()}] Failed to set element as \'{element}\'. " +
                    f"There are too many bonds that cannot be removed.", self.get_id())
            j = 0
            while n < len(self.get_bonds()):
                i = h.pop(0)
                self.bonds.pop(i - j)
                j += 1

    def set_lone_electron(self, lone_electron: int, auto_modify: bool = False) -> None:
        """
        Set the lone_electron attribute to a new number.

        Args:
            lone_electron (int): new number of lone electrons you want to assign to the lone_electron attribute.
            auto_modify (bool): Whether to automatically adjust the number of lone electrons. Default to False.

        Raises:
            AtomError
            BondError
            LoneElectronError
        """
        self.survive()
        n, lone_electron_ = Atom.__bond_num(self.get_element(), self.get_charge(),
                                            lone_electron, Atom.__remove_hydro(self.get_bonds()), self.get_id(),
                                            auto_modify)
        self.lone_electron = lone_electron_
        while n > len(self.get_bonds()):
            hydro = Atom(bonds=[self.id], bond_=False)
            self.bonds.append(hydro.get_id())
        if n < len(self.get_bonds()):
            count_h = 0
            h = []
            for i, a in enumerate(self.get_bonds()):
                if Atom.get_atom(a).get_element() == "H":
                    count_h += 1
                    h.append(i)
            if count_h < len(self.get_bonds()) - n:
                raise LoneElectronError(
                    f"[Atom {self.get_id()}] Failed to set {lone_electron} lone electrons. "
                    .replace("1 lone electrons", "1 lone electron") +
                    f"There are too many bonds that cannot be removed.", self.get_id())
            j = 0
            while n < len(self.get_bonds()):
                i = h.pop(0)
                self.bonds.pop(i - j)
                j += 1

    def survive(self) -> None:
        if Atom.id_map.get(self.id, None) is None:
            raise AtomError(
                f"[Non-existent Atom {self.id}] Atom {self.id} does not exist.", self.id)


class AtomError(Exception):
    atom: int
    message: str

    def __init__(self, message: str, atom: int):
        self.message = message
        self.atom = atom
        super().__init__(self.message)


class BondError(Exception):
    atom: int
    message: str

    def __init__(self, message: str, atom: int):
        self.message = message
        self.atom = atom
        super().__init__(self.message)


class ChargeError(Exception):
    atom: int
    message: str

    def __init__(self, message: str, atom: int):
        self.message = message
        self.atom = atom
        super().__init__(self.message)


class ElementError(Exception):
    atom: int
    message: str

    def __init__(self, message: str, atom: int):
        self.message = message
        self.atom = atom
        super().__init__(self.message)


class IdError(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class LoneElectronError(Exception):
    atom: int
    message: str

    def __init__(self, message: str, atom: int):
        self.message = message
        self.atom = atom
        super().__init__(self.message)


bond: Callable = Atom.bond
break_bond: Callable = Atom.break_bond
delete_atom: Callable = Atom.delete_atom
get_all_atoms: Callable = Atom.get_all_atoms
get_atom: Callable = Atom.get_atom
get_atom_id: Callable = Atom.get_atom_id
reset_tags: Callable = Atom.reset_tags

if __name__ == "__main__":

    import subprocess
    import os
    import shutil
    import ast
    import time

    file_name = os.path.basename(__file__)[:-3]
    destination = 'Test'

    directories_to_remove = ['.mypy_cache', 'build', 'cash', 'out']
    for dir_ in directories_to_remove:
        if os.path.exists(dir_) and os.path.isdir(dir_):
            shutil.rmtree(dir_)

    files_to_remove = [f'{file_name}.pyx', f'{file_name}.c', 'set.py',
                       f'{file_name}.html', f'{file_name + "_cash"}.py']
    for file in files_to_remove:
        if os.path.exists(file) and os.path.isfile(file):
            os.remove(file)

    with open(f'{file_name + "_cash"}.py', 'w', encoding="utf-8") as py_cash:
        with open(f'{file_name}.py', 'r', encoding="utf-8") as py_file:
            all_ = py_file.read()
            all_ = all_[:all_.find('if __name__ == "__main__":')]
            py_cash.write(all_)
            try:
                with open(f'{destination}/_last', 'r', encoding="utf-8") as last:
                    last_ = last.read()
                    time_ = last_[:last_.find("->")]
                    last_ = last_[last_.find("->")+3:]
                    do_ = (last_ != all_)
                if do_:
                    with open(f'{destination}/_last', 'w', encoding="utf-8") as last:
                        last.write(time.strftime("%Y.%m.%d_%H.%M.%S", time.localtime(time.time())) + "->\n" + all_)
                        os.makedirs(f'{destination}/{file_name}_{time_}')
                        for file in os.listdir(destination):
                            if file.endswith('.pyd') and file.startswith(f'{file_name}.'):
                                shutil.move(f'{destination}/{file}', f'{destination}/{file_name}_{time_}')
                        if os.path.exists(f'{destination}/{file_name}.pyi'):
                            shutil.move(f'{destination}/{file_name}.pyi', f'{destination}/{file_name}_{time_}')
                        with open(f'{destination}/{file_name}_{time_}/_source', 'w', encoding="utf-8") as source:
                            source.write(all_)
            except FileNotFoundError:
                with open(f'{destination}/_last', 'w', encoding="utf-8") as last:
                    last.write(time.strftime("%Y.%m.%d_%H.%M.%S", time.localtime(time.time())) + "->\n" + all_)

    print(f'Generating {file_name}.pyi...')
    subprocess.run(['stubgen', f'{file_name + "_cash"}.py'])

    os.rename(f'out/{file_name + "_cash"}.pyi', f'out/{file_name}.pyi')


    class NodePathRecorder(ast.NodeVisitor):
        def __init__(self):
            self.path = []
            self.find = []

        def record_path(self, node):
            try:
                self.path.append(node.name)
            except AttributeError:
                self.path.append("")

        def generic_visit(self, node):
            # noinspection PyTypeChecker
            self.record_path(node)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # noinspection PyTypeChecker
                docstring = ast.get_docstring(node)
                if docstring:
                    self.find.append((".".join([i for i in self.path if i != ""]), docstring, len(self.path),
                                      "class" if isinstance(node, ast.ClassDef) else "func"))
            super().generic_visit(node)
            self.path.pop()


    with open(f'{file_name + "_cash"}.py', 'r', encoding="utf-8") as py_file:
        tree = ast.parse(py_file.read())

    recorder = NodePathRecorder()
    recorder.visit(tree)
    find = recorder.find


    class NodePathRecorder2(ast.NodeVisitor):
        def __init__(self):
            self.path = []
            self.find = ""
            self.return_ = []

        def set(self, find_):
            self.find = find_
            self.return_ = []

        def record_path(self, node):
            try:
                self.path.append(node.name)
            except AttributeError:
                self.path.append("")

        def generic_visit(self, node):
            # noinspection PyTypeChecker
            self.record_path(node)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ".".join([i for i in self.path if i != ""]) == self.find:
                    self.return_.append(node.lineno)
            super().generic_visit(node)
            self.path.pop()


    def indent_string(s, n):
        lines = s.splitlines()
        indented_lines = [n * "    " + line for line in lines]
        indented_string = '\n'.join(indented_lines)
        return indented_string + "\n"


    recorder2 = NodePathRecorder2()
    for i_ in find:
        with open(f"out/{file_name}.pyi", 'r', encoding="utf-8") as pyi_file:
            tree2 = ast.parse(pyi_file.read())
        recorder2.set(i_[0])
        recorder2.visit(tree2)
        with open(f'out/{file_name}.pyi', 'r', encoding='utf-8') as atom_i_file:
            atom_i_content = atom_i_file.readlines()
        with open(f'out/{file_name}.pyi', 'w', encoding='utf-8') as atom_i_file:
            atom_i_file.writelines(atom_i_content[:recorder2.return_[0] - 1])
            if i_[3] == "class":
                atom_i_file.write(atom_i_content[recorder2.return_[0] - 1])
                atom_i_file.write(indent_string('"""\n' + i_[1] + '\n"""\n', i_[2] - 1))
            else:
                atom_i_file.write(atom_i_content[recorder2.return_[0] - 1][:-5] + '\n')
                atom_i_file.write(indent_string('"""\n' + i_[1] + '\n"""\n...\n', i_[2] - 1))
            atom_i_file.writelines(atom_i_content[recorder2.return_[0]:])

    print(f'Generating {file_name}.pyx...')
    with open(f'{file_name}.pyx', 'w', encoding="utf-8") as pyx_file:
        pyx_file.write('# -*- coding: utf-8 -*-\n')
        pyx_file.write('# cython: language_level=3\n\n')
        with open(f'{file_name + "_cash"}.py', 'r', encoding="utf-8") as py_file:
            pyx_file.write(py_file.read())

    print(f'Building {file_name}.pyd...')
    set_up = f'from setuptools import setup\nfrom Cython.Build import cythonize\nsetup(\n' \
             f'    ext_modules=cythonize("{file_name}.pyx")\n)'
    with open("set.py", "w", encoding="utf-8") as set_:
        set_.write(set_up)

    subprocess.run(['python', 'set.py', 'build_ext', '--inplace'])

    directories_to_remove = ['.mypy_cache', 'build']
    for dir_ in directories_to_remove:
        if os.path.exists(dir_) and os.path.isdir(dir_):
            shutil.rmtree(dir_)

    file_find = None
    for file in os.listdir('.'):
        if file.endswith('.pyd') and file.startswith(f'{file_name}.'):
            file_find = file
            break

    if not os.path.exists(destination):
        os.makedirs(destination)

    os.makedirs("cash")
    files_to_move = [file_find, f'out/{file_name}.pyi']
    for file in files_to_move:
        shutil.move(file, "cash")

    files_to_remove = [f'{file_name}.pyx', f'{file_name}.c', f"{destination}/{file_find}",
                       f"{destination}/{file_name}.pyi", 'set.py',
                       f'{file_name}.html', f'{file_name + "_cash"}.py']
    for file in files_to_remove:
        if os.path.exists(file) and os.path.isfile(file):
            os.remove(file)

    files_to_move = [f'cash/{file_find}', f'cash/{file_name}.pyi']
    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, destination)

    shutil.rmtree('cash')

    if os.path.exists('out') and os.path.isdir('out'):
        shutil.rmtree('out')
