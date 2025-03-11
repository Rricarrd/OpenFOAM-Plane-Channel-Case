/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2019-2021 OpenCFD Ltd.
    Copyright (C) YEAR AUTHOR, AFFILIATION
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "functionObjectTemplate.H"
#define namespaceFoam  // Suppress <using namespace Foam;>
#include "fvCFD.H"
#include "unitConversion.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

defineTypeNameAndDebug(CfFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    CfFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = da05624419f33946654458100a5c0b3cf01e2370
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void Cf_da05624419f33946654458100a5c0b3cf01e2370(bool load)
{
    if (load)
    {
        // Code that can be explicitly executed after loading
    }
    else
    {
        // Code that can be explicitly executed before unloading
    }
}


// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode

} // End namespace Foam


// * * * * * * * * * * * * * Private Member Functions  * * * * * * * * * * * //

const Foam::fvMesh&
Foam::CfFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
CfFunctionObject::
CfFunctionObject
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    functionObjects::regionFunctionObject(name, runTime, dict)
{
    read(dict);
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
CfFunctionObject::
~CfFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool
Foam::
CfFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        printMessage("read Cf");
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool
Foam::
CfFunctionObject::execute()
{
    if (false)
    {
        printMessage("execute Cf");
    }

//{{{ begin code
    #line 45 "/home/rricarrd/OpenFOAM/rricarrd-v2412/run/planeChannel/basicCase/system/controlDict/functions/Cf"
auto* CfPtr =
                mesh().getObjectPtr<volScalarField>("Cf");

            if (!CfPtr)
            {
                Info<< "Create skin-friction coefficient field" << nl;
                CfPtr = new volScalarField
                (
                    IOobject
                    (
                        "Cf",
                        mesh().time().timeName(),
                        mesh(),
                        IOobject::NO_READ,
                        IOobject::AUTO_WRITE,
                        IOobject::REGISTER
                    ),
                    mesh(),
                    dimless
                );

                regIOobject::store(CfPtr);
            }

            auto& Cf = *CfPtr;

            Info<< "Computing skin-friction coefficient field\n" << endl;

            const auto& tau =
                mesh().lookupObject<volVectorField>("wallShearStress");

            const dimensionedScalar Ubulk(dimVelocity, 17.55);

            Cf = mag(tau.component(0))/(0.5*sqr(Ubulk));
//}}} end code

    return true;
}


bool
Foam::
CfFunctionObject::write()
{
    if (false)
    {
        printMessage("write Cf");
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool
Foam::
CfFunctionObject::end()
{
    if (false)
    {
        printMessage("end Cf");
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// ************************************************************************* //

