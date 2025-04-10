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

defineTypeNameAndDebug(ReTauFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    ReTauFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = 1618721f2c13852d61b4a9ffca6c0f8495853ba5
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void ReTau_1618721f2c13852d61b4a9ffca6c0f8495853ba5(bool load)
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
Foam::ReTauFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
ReTauFunctionObject::
ReTauFunctionObject
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
ReTauFunctionObject::
~ReTauFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool
Foam::
ReTauFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        printMessage("read ReTau");
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool
Foam::
ReTauFunctionObject::execute()
{
    if (false)
    {
        printMessage("execute ReTau");
    }

//{{{ begin code
    #line 33 "/home/rricarrd/OpenFOAM/rricarrd-v2412/run/planeChannelVariations/basicCase/system/controlDict/functions/ReTau"
auto* ReTauPtr =
                mesh().getObjectPtr<volScalarField>("ReTau");

            if (!ReTauPtr)
            {
                Info<< "Create a Re tau field" << nl;
                ReTauPtr = new volScalarField
                (
                    IOobject
                    (
                        "ReTau",
                        mesh().time().timeName(),
                        mesh(),
                        IOobject::NO_READ,
                        IOobject::AUTO_WRITE,
                        IOobject::REGISTER
                    ),
                    mesh(),
                    dimless
                );

                regIOobject::store(ReTauPtr);
            }

            auto& ReTau = *ReTauPtr;

            Info<< "Computing Re tau field\n" << endl;

            const auto& tau = mesh().lookupObject<volVectorField>("wallShearStress");
            
            const dimensionedScalar h(dimLength, 1.0);
            
            const dimensionedScalar nu(sqr(dimLength)/dimTime, 0.0002);
            
            const dimensionedScalar Ubulk(dimVelocity, 1);
            
            ReTau = sqrt(mag(tau.component(0)))*h/nu;
            
            // Get mesh patch ids
            label patchIDtop = mesh().boundaryMesh().findPatchID("top");
            
            Info << "Patch id top: " << patchIDtop << endl;
            
            label patchIDbottom = mesh().boundaryMesh().findPatchID("bottom");

            
            // Compute the average of ReTau
            scalar sumReTau = (gSum(ReTau.boundaryField()[patchIDtop]) + gSum(ReTau.boundaryField()[patchIDbottom]))/2;
            
            Info << "sumReTau " << sumReTau << endl;
            
            scalar nodes = 1024;
            
            Info << "nodes: " << nodes << endl;
            
            scalar avgReTau = sumReTau / nodes;

            // Print the average value to the console
            Info << "Average ReTau: " << avgReTau << endl;
//}}} end code

    return true;
}


bool
Foam::
ReTauFunctionObject::write()
{
    if (false)
    {
        printMessage("write ReTau");
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool
Foam::
ReTauFunctionObject::end()
{
    if (false)
    {
        printMessage("end ReTau");
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// ************************************************************************* //

