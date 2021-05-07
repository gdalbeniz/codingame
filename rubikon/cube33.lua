

strS = {"U", "F", "R", "B", "L", "D"}
strM = {"U", "F", "R", "B", "L", "D", "u", "f", "r", "z"}
strC = {"W", "G", "R", "B", "O", "Y", "?"}

S = {U=1, F=2, R=3, B=4, L=5, D=6}
M = {U=1, F=2, R=3, B=4, L=5, D=6, u=7, f=8, r=9, z=10}
C = {W=1, G=2, R=3, B=4, O=5, Y=6, k=7}

AM = {M.U, M.F, M.R, M.B, M.L, M.D, M.z}

solved = {
--Up/White  [1]  [2]  [3]
    {
        [1]={C.W, C.W, C.W},
        [2]={C.W, C.W, C.W},
        [3]={C.W, C.W, C.W}
    },
--Front/Green [1] [2]  [3]
    {
        [1]={C.G, C.G, C.G},
        [2]={C.G, C.G, C.G},
        [3]={C.G, C.G, C.G}
    },
--Right/Red  [1]  [2]  [3]
    {
        [1]={C.R, C.R, C.R},
        [2]={C.R, C.R, C.R},
        [3]={C.R, C.R, C.R}
    },
--Back/Blue [1]  [2]  [3]
    {
        [1]={C.B, C.B, C.B},
        [2]={C.B, C.B, C.B},
        [3]={C.B, C.B, C.B}
    },
--Left/Orange [1] [2]  [3]
    {
        [1]={C.O, C.O, C.O},
        [2]={C.O, C.O, C.O},
        [3]={C.O, C.O, C.O}
    },
--Down/Yellow [1] [2]  [3]
    {
        [1]={C.Y, C.Y, C.Y},
        [2]={C.Y, C.Y, C.Y},
        [3]={C.Y, C.Y, C.Y}
    }
}
initial = {
--Up/White  [1]  [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.k, C.k, C.k},
        [3]={C.k, C.k, C.k}
    },
--Front/Green [1] [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.G, C.G, C.B},
        [3]={C.G, C.G, C.G}
    },
--Right/Red  [1]  [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.R, C.R, C.R},
        [3]={C.R, C.R, C.R}
    },
--Back/Blue [1]  [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.G, C.B, C.B},
        [3]={C.B, C.B, C.B}
    },
--Left/Orange [1] [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.O, C.O, C.O},
        [3]={C.O, C.O, C.O}
    },
--Down/Yellow [1] [2]  [3]
    {
        [1]={C.Y, C.Y, C.Y},
        [2]={C.Y, C.Y, C.Y},
        [3]={C.Y, C.Y, C.Y}
    }
}
final = {
--Up/White  [1]  [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.k, C.k, C.k},
        [3]={C.k, C.k, C.k}
    },
--Front/Green [1] [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.G, C.G, C.G},
        [3]={C.G, C.G, C.G}
    },
--Right/Red  [1]  [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.R, C.R, C.R},
        [3]={C.R, C.R, C.R}
    },
--Back/Blue [1]  [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.B, C.B, C.B},
        [3]={C.B, C.B, C.B}
    },
--Left/Orange [1] [2]  [3]
    {
        [1]={C.k, C.k, C.k},
        [2]={C.O, C.O, C.O},
        [3]={C.O, C.O, C.O}
    },
--Down/Yellow [1] [2]  [3]
    {
        [1]={C.Y, C.Y, C.Y},
        [2]={C.Y, C.Y, C.Y},
        [3]={C.Y, C.Y, C.Y}
    }
}

-- all
function rota_side(cube, side, n)
    local s = cube[side]
    for _ = 1,n do
        local t = s[1][1]
        s[1][1] = s[3][1]
        s[3][1] = s[3][3]
        s[3][3] = s[1][3]
        s[1][3] = t
        local t = s[1][2]
        s[1][2] = s[2][1]
        s[2][1] = s[3][2]
        s[3][2] = s[2][3]
        s[2][3] = t
    end
end

-- U, u, D
function rota_layer(cube, layer, n)
    local c = cube
    local l = layer
    for _ = 1,n do
        local t = c[2][l]
        c[2][l] = c[3][l]
        c[3][l] = c[4][l]
        c[4][l] = c[5][l]
        c[5][l] = t
    end
end
--[[  check if more performant???
    if n == 1 then
        local t = c[2][l]
        c[2][l] = c[3][l]
        c[3][l] = c[4][l]
        c[4][l] = c[5][l]
        c[5][l] = t
    elseif n == 2 then
        local t = c[2][l]
        c[2][l] = c[4][l]
        c[4][l] = t
        local t = c[3][l]
        c[3][l] = c[5][l]
        c[5][l] = t
    elseif n == 3 then
        local t = c[2][l]
        c[2][l] = c[5][l]
        c[5][l] = c[4][l]
        c[4][l] = c[3][l]
        c[3][l] = t
    end
]]

-- R, r, L
function rota_slice(cube, slice, n)
    local c = cube
    local s = slice
    local r = 4 - s
    for _ = 1,n do
        local t = c[1][1][r]
        c[1][1][r] = c[2][1][r]
        c[2][1][r] = c[6][1][r]
        c[6][1][r] = c[4][3][s]
        c[4][3][s] = t
        local t = c[1][2][r]
        c[1][2][r] = c[2][2][r]
        c[2][2][r] = c[6][2][r]
        c[6][2][r] = c[4][2][s]
        c[4][2][s] = t
        local t = c[1][3][r]
        c[1][3][r] = c[2][3][r]
        c[2][3][r] = c[6][3][r]
        c[6][3][r] = c[4][1][s]
        c[4][1][s] = t
    end
end

-- F, f, B
function rota_face(cube, face, n)
    local c = cube
    local f = face
    local g = 4 - f
    for _ = 1,n do
        local t = c[1][g][1]
        c[1][g][1] = c[5][3][g]
        c[5][3][g] = c[6][f][3]
        c[6][f][3] = c[3][1][f]
        c[3][1][f] = t
        local t = c[1][g][2]
        c[1][g][2] = c[5][2][g]
        c[5][2][g] = c[6][f][2]
        c[6][f][2] = c[3][2][f]
        c[3][2][f] = t
        local t = c[1][g][3]
        c[1][g][3] = c[5][1][g]
        c[5][1][g] = c[6][f][1]
        c[6][f][1] = c[3][3][f]
        c[3][3][f] = t
    end
end


-- rotate
function rota(cube, mov, n)
    if mov == M.U then -- upper layer
        rota_side(cube, S.U, n)
        rota_layer(cube, 1, n)
    elseif mov == M.R then -- right slice
        rota_side(cube, S.R, n)
        rota_slice(cube, 1, n)
    elseif mov == M.F then -- front face
        rota_side(cube, S.F, n)
        rota_face(cube, 1, n)
    elseif mov == M.L then -- left slice
        rota_side(cube, S.L, n)
        rota_slice(cube, 3, 4-n)
    elseif mov == M.D then -- down layer
        rota_side(cube, S.D, n)
        rota_layer(cube, 3, 4-n)
    elseif mov == M.B then -- back face
        rota_side(cube, S.B, n)
        rota_face(cube, 3, 4-n)
    elseif mov == M.u then -- middle layer
        rota_layer(cube, 2, n)
    elseif mov == M.r then -- middle slice
        rota_slice(cube, 2, n)
    elseif mov == M.f then -- middle face
        rota_face(cube, 2, n)
    elseif mov == M.z then -- whole cube
        rota_side(cube, S.U, n)
        rota_layer(cube, 1, n)
        rota_layer(cube, 2, n)
        rota_layer(cube, 3, n)
        rota_side(cube, S.D, 4-n)
    else
        print("INVALID MOVE")
    end
end

function cube_copy(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in next, orig, nil do
            copy[cube_copy(orig_key)] = cube_copy(orig_value)
        end
        setmetatable(copy, cube_copy(getmetatable(orig)))
    else -- number, string, boolean, etc
        copy = orig
    end
    return copy
end

function cube_reset(cube, from)
    local from = from or solved
    for i = 1,6 do
        for j = 1,3 do
            for k = 1,3 do
                cube[i][j][k] = from[i][j][k]
            end
        end
    end
end


function cube_genmovs(availmovs, depth)
    local movs = {}
    for i = 1,depth do
        for m in availmovs do
            if m == last_m
            for n = 1,3 do

    end


end

function cube_apply(cube, movs)
    for i in movs do
        rota(cube, i.m, i.n)
    end
end

function cube_applystr(cube, movstr)
    -- todo convert movstr
    cube_apply(cube, movs)
end


function print_side(cube, i)
    local side = cube[i]
    print("-side " .. strS[i])
    for j, line in ipairs(side) do
        linestr = string.format("--line %d : %s %s %s", j, strC[line[1]], strC[line[2]], strC[line[3]])
        print(linestr)
    end
end

function print_cube(cube)
    for i = 1,6 do
        print_side(cube, i)
    end
end

function cube_equal(cube1, cube2)
    local equal = true
    for i = 1,6 do
        local side1, side2 = cube1[i], cube2[i]
        for j = 1,3 do
            local line1, line2 = side1[j], side2[j]
            for k = 1,3 do
                local col1, col2 = line1[k], line2[k]
                if col1 ~= col2 and col1 ~= C.k and col2 ~= C.k then
                    equal = false
                    break
                end
            end
        end
    end
    return equal
end




function cube_solve(initial, final, movements, max_movs, num_sols)
    local movements = movements or M
    local max_movs = max_movs or 24
    local num_sols = num_sols or 1

    solutions = {}
    chains = {} --todo create generator
    for i = 1,max_movs do
        for chain in chains do
            --i
        end
    end
    return solutions
end


--[[
rota(solved, M.U, 1)
rota(solved, M.R, 1)
rota(solved, M.U, 3)
rota(solved, M.R, 3)
rota(solved, M.U, 3)
rota(solved, M.F, 3)
rota(solved, M.U, 1)
rota(solved, M.F, 1)
]]
--[[
rota(solved, M.U, 3)
rota(solved, M.L, 3)
rota(solved, M.U, 1)
rota(solved, M.L, 1)
rota(solved, M.U, 1)
rota(solved, M.F, 1)
rota(solved, M.U, 3)
rota(solved, M.F, 3)
]]

--[[
rota(solved, M.B, 1)
rota(solved, M.D, 1)
rota(solved, M.F, 3)
rota(solved, M.u, 1)
]]
--rota(solved, M.z, 1)

--apply(solved, "U R U' R' U' F' U F")

print_cube(solved)

print("solved ? initial is ", cube_equal(solved, initial))
print("solved ? final is ", cube_equal(solved, final))
print("solved ? solved is ", cube_equal(solved, solved))