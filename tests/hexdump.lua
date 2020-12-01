function dump(val, width)
	if val == nil then val = 0 end
	if width == nil then width = 1 end
	for i=1, width do -- little endian
		local shift = ((i - 1) * 8)
		local mask = 0xFF << shift
		io.write(string.format("%02X ", (val & mask) >> shift))
	end
end

function hex(val, width)
	dump(val, width)
	print()
end

function hexs(str)
	-- convert string to a stream of hex values
	for c in str:gmatch(".") do
		dump(c:byte())
	end
	print()
end

return 2
