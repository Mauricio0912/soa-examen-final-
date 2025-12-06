package com.dmaf.apirest.service;

import com.dmaf.apirest.model.Curso;
import com.dmaf.apirest.repository.CursoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class CursoService {

    @Autowired
    private CursoRepository cursoRepository;

    public List<Curso> listarTodos() {
        return cursoRepository.findAll();
    }

    public Optional<Curso> obtenerPorId(Long id) {
        return cursoRepository.findById(id);
    }

    public Curso crear(Curso curso) {
        return cursoRepository.save(curso);
    }

    public Optional<Curso> actualizar(Long id, Curso cursoActualizado) {
        return cursoRepository.findById(id).map(curso -> {
            curso.setNombre(cursoActualizado.getNombre());
            curso.setDescripcion(cursoActualizado.getDescripcion());
            curso.setFechaInicio(cursoActualizado.getFechaInicio());
            curso.setFechaFin(cursoActualizado.getFechaFin());
            return cursoRepository.save(curso);
        });
    }

    public boolean eliminar(Long id) {
        if (cursoRepository.existsById(id)) {
            cursoRepository.deleteById(id);
            return true;
        }
        return false;
    }

    public List<Curso> buscarPorNombre(String nombre) {
        return cursoRepository.findByNombreContainingIgnoreCase(nombre);
    }

    public List<Curso> buscarPorFechaInicio(LocalDate fechaInicio) {
        return cursoRepository.findByFechaInicio(fechaInicio);
    }
}
