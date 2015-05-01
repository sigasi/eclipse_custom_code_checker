library ieee;
use ieee.std_logic_1164.all;
package constants is

	constant MAX_COUNT : integer := 2 ** 8 - 1; -- ( ( 2 ** 8) - 1 == 255

	constant ANSWER : integer := 4 * 10 + 2; -- (4 * 10) + 2 == 42

end package constants;
