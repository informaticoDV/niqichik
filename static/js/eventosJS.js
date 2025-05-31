(function(){
    const btnEliminacion=document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn=>{
        btn.addEventListener('click',(e)=>{
            const confirmacion=confirm('¿Seguro que quiere eliminar la tarea?');
            if(!confirmacion){
                e.preventDefault();
            }
        });
    });

    const btnPagar=document.querySelectorAll(".btnPagar");

    btnPagar.forEach(btn=>{
        btn.addEventListener('click',(e)=>{
            const confirmacion=confirm('¿Confirma que la tarea se desempeño en su totalidad?');
            if(!confirmacion){
                e.preventDefault();
            }
        });
    });

    const btnAsignar=document.querySelectorAll(".btnAsignar");

    btnAsignar.forEach(btn=>{
        btn.addEventListener('click',(e)=>{
            const confirmacion=confirm('¿Esta seguro que desea continuar?');
            if(!confirmacion){
                e.preventDefault();
            }
        });
    });

})();