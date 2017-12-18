<?php

namespace AppBundle\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\NumberType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\FileType;
use Symfony\Bridge\Doctrine\Form\Type\EntityType;

class TipoEvento extends AbstractType {
    
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
       $builder
            ->add('latitud', get_class(new NumberType),
                    array(
                        'required' => true
                         )  
                 )
            ->add('longitud', get_class(new NumberType),
                    array(
                        'required' => true
                         )  
                 )
            ->add('nombreAfectacion', 'entity' ,array(
                'class' => 'AppBundle:Afectacion',
                'choice_label' => 'nombre',
                'multiple' => true,
                'expanded' => true,
                'required' => true
                         )
                  )
            ->add('fenomeno', get_class(new ChoiceType),array(
                'choices' => array(
                                'Inundacion' => 'Inundacion', 
                                'Lluvia' => 'Lluvia',
                                'Tormenta' => 'Tormenta',
                                'Llovizna' => 'Llovizna',
                                'Viento' => 'Viento',
                                'Nieve' => 'Nieve',
                                'Granizo' => 'Granizo',
                                'Actividad Electrica' => 'Actividad Electrica'),
                'choices_as_values' => true,
                'required' => true
                        )
                 );
       
    }
  
}